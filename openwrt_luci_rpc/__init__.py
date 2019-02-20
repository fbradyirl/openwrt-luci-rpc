# -*- coding: utf-8 -*-

"""Top-level package for openwrt-luci-rpc."""

__author__ = """Finbarr Brady"""
__email__ = 'fbradyirl@github.io'
__version__ = '0.4.6'

from .openwrt_luci_rpc import OpenWrtLuciRPC
from .constants import OpenWrtConstants


class OpenWrtRpc:
    """
    Class to interact with OpenWrt router running luci-mod-rpc package.
    """

    def __init__(self, host_url=OpenWrtConstants.DEFAULT_LOCAL_HOST_URL,
                 username=OpenWrtConstants.DEFAULT_USERNAME,
                 password=OpenWrtConstants.DEFAULT_PASSWORD):
        """
        Initiate an instance with a default local ip (192.168.1.1)
        :param host_url: string - host url. Defaults to 192.168.1.1
        :param username: string - username. Defaults to root
        :param password: string - password. Default is blank
        """
        self.router = OpenWrtLuciRPC(host_url, username, password)

    def is_logged_in(self):
        """Returns true if a token has been aquired"""
        return self.router.token is not None

    def get_all_connected_devices(self, only_reachable=True):
        """Get details of all devices"""
        return self.router.get_all_connected_devices(
            only_reachable=only_reachable)
