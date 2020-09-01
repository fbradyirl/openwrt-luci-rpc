# -*- coding: utf-8 -*-

"""
Support for OpenWrt (luci) routers.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/device_tracker.luci/
"""

import requests
import json
import logging

from packaging import version
from collections import namedtuple
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from openwrt_luci_rpc import utilities
from .constants import Constants
from .exceptions import InvalidLuciTokenError, \
    LuciRpcMethodNotFoundError, InvalidLuciLoginError, \
    LuciRpcUnknownError, PageNotFoundError, LuciConfigError

log = logging.getLogger(__name__)


class OpenWrtLuciRPC:

    def __init__(self, host, username, password, is_https, verify_https):
        """
        Initiate an API request with all parameters
        :param host: string
        :param username: string
        :param password: string
        :param is_https: boolean
        :param verify_https: boolean
        """

        if not host:
            raise LuciConfigError('host cannot be empty. '
                                  'Use the IP or hostname of your'
                                  'OpenWrt router')

        if not is_https:
            protocol = 'http'
        else:
            protocol = 'https'

            if not verify_https:
                requests.packages.urllib3.disable_warnings(
                    InsecureRequestWarning
                )

        self.host = host
        self.host_api_url = '{}://{}'.format(protocol, host)
        self.username = username
        self.password = password
        self.verify_https = verify_https
        self.session = requests.Session()
        self.token = None
        self.owrt_version = None
        self._refresh_token()
        self.is_legacy_version, self.arp_call \
            = self._determine_if_legacy_version()

    def _refresh_token(self):
        """Get authentication token for the given configuration."""
        auth_url = Constants.\
            LUCI_RPC_LOGIN_PATH.format(self.host_api_url)
        self.token = self._call_json_rpc(auth_url, 'login',
                                         self.username, self.password)
        log.info("Luci RPC login was successful")

    def _determine_if_legacy_version(self):
        """
        * Checks to see if we are running a pre-18.06 version

        :return: tuple, with True if legacy and the URL to
                use to lookup devices
        """

        log.info("Getting OpenWRT version")

        # NEW METHOD TO DETERMINE OPENWRT VERSION EXACTLY
        # TODO: Check as non-root user

        # get VERSION_ID from os-release if exists or get
        # DISTRIB_RELEASE from openwrt_release
        shell_command = "if [ -f \"/etc/os-release\" ]; \
                            then awk -F= '$1==\"VERSION_ID\" \
                            { print $2 ;}' \
                            /etc/os-release; \
                            else awk -F= '$1==\"DISTRIB_RELEASE\" \
                            { print $2 ;}' \
                            /etc/openwrt_release; fi | \
                            tr -d \\'\\\""

        rcp_sys_version_call = Constants.\
            LUCI_RPC_SYS_PATH.format(self.host_api_url), "exec"

        try:
            content = self._call_json_rpc(rcp_sys_version_call[0],
                                          rcp_sys_version_call[1],
                                          shell_command)   # type: str

            content = content.replace("\n", "")

            if content is None:
                raise LuciRpcUnknownError("could not \
                determine openwrt version")

            self.owrt_version = version.parse(content.strip())
        except InvalidLuciLoginError:
            log.info("Refreshing login token")
            self._refresh_token()
            return self._determine_if_legacy_version()
        except Exception:
            log.error("Could not determine OpenWRT version, \
                         defaulting to version 18.06")
            self.owrt_version = version.parse("18.06")

        rpc_sys_arp_call = Constants.\
            LUCI_RPC_SYS_PATH.format(self.host_api_url), 'net.arptable'
        rpc_ip_call = Constants.\
            LUCI_RPC_IP_PATH.format(
                self.host_api_url), 'neighbors', {"family": 4}

        if self.owrt_version != version.parse("snapshot") and self.owrt_version < version.parse("18.06"):  # noqa: E501
            return True, rpc_sys_arp_call
        else:
            return False, rpc_ip_call

    def get_all_connected_devices(self, only_reachable, wlan_interfaces):
        """
        Get details of all connected devices.

        Notes around newer OpenWrt releases (18.06+)

            Do not use `reachable` or `stale` values
            as they flap constantly even
            when the device is inside the network.
            The very existence of the mac in the results
            is enough to determine the "device is home"

        :param only_reachable: boolean, if true,
               only return devices which are reachable
               (this is for 17.06 or earlier only. 18+
               does not have a proper ability to determine
               this, as above)
        """
        log.debug("Checking for connected devices")
        last_results = []
        # rpc_sys__winfo_call = Constants.\
        #     LUCI_RPC_SYS_PATH.format(self.host_api_url), \
        #                       'wifi.getiwinfo', wlan_interfaces
        rpc_uci_call = Constants.LUCI_RPC_UCI_PATH.format(
            self.host_api_url), 'get_all', 'dhcp'

        try:
            # First, try find the associated wifi devices
            # winfo_result = self._call_json_rpc(*rpc_sys__winfo_call)
            arp_result = self._call_json_rpc(*self.arp_call)
            dhcp_result = self._call_json_rpc(*rpc_uci_call)
        except InvalidLuciTokenError:
            log.info("Refreshing login token")
            self._refresh_token()
            return self.get_all_connected_devices(only_reachable,
                                                  wlan_interfaces)

        for device_entry in arp_result:
            if device_entry is None:
                continue

            device_entry = utilities.normalise_keys(device_entry)

            if "mac" not in device_entry:
                continue

            device_entry['hostname'] = utilities.get_hostname_from_dhcp(
                dhcp_result, device_entry['mac'])

            # As a convenience, add the router IP as the host
            # for every device. Can be useful when a network has more
            # than one router.
            if "host" not in device_entry:
                device_entry['host'] = self.host

            device = namedtuple("Device", device_entry.keys())(
                *device_entry.values())

            if "Flags" in device_entry and only_reachable:
                # Check if the Flags for each device contain
                # NUD_REACHABLE and if not, skip.
                if not int(device_entry['Flags'], 16) & 0x2:
                    continue

            last_results.append(device)

        log.debug(last_results)
        return last_results

    def _call_json_rpc(self, url, method, *args, **kwargs):
        """Perform one JSON RPC operation."""
        data = json.dumps({'method': method, 'params': args})

        # pass token to make it work with versions < 17
        if self.token is not None:
            url += "?auth=" + self.token

        log.debug("_call_json_rpc : %s" % url)
        res = self.session.post(url,
                                data=data,
                                timeout=Constants.DEFAULT_TIMEOUT,
                                verify=self.verify_https,
                                **kwargs)

        if res.status_code == 200:
            result = res.json()
            try:
                content = result['result']

                if content is not None:
                    return content

                elif result['error'] is not None:
                    # On 18.06, we want to check for error 'Method not Found'
                    error_message = result['error']['message']
                    error_code = result['error']['code']
                    if error_code == -32601:
                        raise LuciRpcMethodNotFoundError(
                            "method: '%s' returned an "
                            "error '%s' (code: '%s).",
                            method, error_message, error_code)
                else:
                    log.debug("method: '%s' returned : %s" % (method, result))
                    # Authentication error
                    raise InvalidLuciLoginError("Failed to authenticate "
                                                "with Luci RPC, check your "
                                                "username and password.")

            except KeyError:
                raise LuciRpcUnknownError("No result in response from luci")

        elif res.status_code == 401:
            raise InvalidLuciLoginError("Failed to authenticate "
                                        "with Luci RPC, check your "
                                        "username and password.")
        elif res.status_code == 403:
            raise InvalidLuciTokenError("Luci responded "
                                        "with a 403 Invalid token")
        elif res.status_code == 404:
            raise PageNotFoundError("404 returned "
                                    "from %s. Ensure you have "
                                    "installed package "
                                    "`luci-mod-rpc`." % url)

        raise LuciRpcUnknownError("Invalid response from luci: %s", res)
