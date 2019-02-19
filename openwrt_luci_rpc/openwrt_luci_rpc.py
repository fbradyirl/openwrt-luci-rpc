# -*- coding: utf-8 -*-

"""
Support for OpenWRT (luci) routers.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/device_tracker.luci/
"""

import requests
import json
import logging

log = logging.getLogger(__name__)


class InvalidLuciTokenError(Exception):
    """When an invalid token is detected."""

    pass


class LuciRpcMethodNotFoundError(Exception):
    """When an invalid method is called."""

    pass


class OpenWrtLuciRPC:

    def __init__(self, host_url, username=None, password=None):
        """
        Initiate an API request with all parameters
        :param host_url: string
        :param username: string
        :param password: string
        """
        self.host_api_url = host_url
        self.username = username
        self.password = password
        self.token = None
        self._refresh_token()

    def _refresh_token(self):
        """Get a new token."""
        self.token = self._get_token()

    def _get_token(self):
        """Get authentication token for the given configuration."""

        url = '{}/cgi-bin/luci/rpc/auth'.format(self.host_api_url)
        return self._call_json_rpc(url, 'login', self.username, self.password)

    def _call_json_rpc(self, url, method, *args, **kwargs):
        """Perform one JSON RPC operation."""
        data = json.dumps({'method': method, 'params': args})

        try:
            log.info("_call_json_rpc : %s" % url)
            res = requests.post(url, data=data, timeout=5, **kwargs)
        except requests.exceptions.Timeout:
            log.exception("Connection to the router timed out")
            return
        if res.status_code == 200:
            try:
                result = res.json()
            except ValueError:
                # If json decoder could not parse the response
                log.exception("Failed to parse response from luci")
                return
            try:
                result_value = result['result']

                if result_value is not None:
                    log.debug("method: '%s' returned : %s" %
                              (method, result_value))
                    return result_value

                elif result['error'] is not None:
                    # On 18.06, we want to check for error 'Method not Found'
                    error_message = result['error']['message']
                    error_code = result['error']['code']
                    log.error(
                        "method: '%s' returned an "
                        "error '%s' (code: '%s).",
                        method, error_message, error_code)
                    if error_code == -32601:
                        raise LuciRpcMethodNotFoundError
                else:
                    log.debug("method: '%s' returned : %s" % (method, result))
                    # Authentication error
                    log.exception("Failed to authenticate "
                                  "with Luci RPC, check your "
                                  "username and password.")
                    return

            except KeyError:
                log.exception("No result in response from luci")
                return
        elif res.status_code == 401:
            # Authentication error
            log.exception(
                "Failed to authenticate, check your username and password")
            return
        elif res.status_code == 403:
            log.error("Luci responded with a 403 Invalid token")
            raise InvalidLuciTokenError

        else:
            log.error("Invalid response from luci: %s", res)
