# -*- coding: utf-8 -*-

"""
Support for OpenWRT (luci) routers.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/device_tracker.luci/
"""

import requests
import json
import logging

from collections import namedtuple
from openwrt_luci_rpc import utilities
from .constants import OpenWrtConstants
from .exceptions import InvalidLuciTokenError, \
    LuciRpcMethodNotFoundError, InvalidLuciLoginError, \
    LuciRpcUnknownError, PageNotFoundError

log = logging.getLogger(__name__)


class OpenWrtLuciRPC:

    def __init__(self, host_url, username, password):
        """
        Initiate an API request with all parameters
        :param host_url: string
        :param username: string
        :param password: string
        """
        self.host_api_url = host_url
        self.username = username
        self.password = password
        self.session = requests.Session()
        self.token = None
        self._refresh_token()
        self.is_legacy_version, self.arp_call \
            = self._determine_if_legacy_version()

    def _refresh_token(self):
        """Get a new token."""
        self.token = self._get_token()

    def _get_token(self):
        """Get authentication token for the given configuration."""

        auth_url = OpenWrtConstants.\
            LUCI_RPC_LOGIN_PATH.format(self.host_api_url)
        return self._call_json_rpc(auth_url, 'login',
                                   self.username, self.password)

    def _determine_if_legacy_version(self):
        """
        * Checks to see if we are running a pre-18.06 version

        :return: tuple, with True if legacy and the URL to
                use to lookup devices
        """
        rpc_sys_call = OpenWrtConstants.\
            LUCI_RPC_SYS_PATH.format(self.host_api_url), 'net.arptable'
        rpc_ip_call = OpenWrtConstants.\
            LUCI_RPC_IP_PATH.format(
                self.host_api_url), 'neighbors', {"family": 4}
        try:
            # Newer OpenWRT releases (18.06+)
            self._call_json_rpc(*rpc_ip_call)
        except PageNotFoundError:
            # This is normal for older OpenWRT (pre-18.06)
            log.info('Determined a pre-18.06 build of OpenWrt')
            return True, rpc_sys_call

        log.info('Determined a 18.06 or newer build of OpenWrt')
        return False, rpc_ip_call

    def get_all_connected_devices(self, only_reachable):
        """
        Get details of all connected devices.

        Notes around newer OpenWRT releases (18.06+)

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
        log.info("Checking for connected devices")
        last_results = []
        rpc_uci_call = OpenWrtConstants.LUCI_RPC_UCI_PATH.format(
            self.host_api_url), 'get_all', 'dhcp'

        try:
            result = self._call_json_rpc(*self.arp_call)
            dhcp_result = self._call_json_rpc(*rpc_uci_call)
        except InvalidLuciTokenError:
            log.info("Refreshing token")
            self._refresh_token()
            return self.get_all_connected_devices()

        if result:
            for device_entry in result:
                utilities.normalise_keys(device_entry)

                if "mac" not in device_entry:
                    continue

                device_entry['hostname'] = utilities.get_hostname_from_dhcp(
                    dhcp_result, device_entry['mac'])
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

        log.info("_call_json_rpc : %s" % url)
        res = self.session.post(url,
                                data=data,
                                timeout=OpenWrtConstants.DEFAULT_TIMEOUT,
                                **kwargs)

        if res.status_code == 200:
            result = res.json()
            try:
                token = result['result']

                if token is not None:
                    log.info("Luci RPC login was successful")
                    return token

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

        else:
            raise LuciRpcUnknownError("Invalid response from luci: %s", res)
