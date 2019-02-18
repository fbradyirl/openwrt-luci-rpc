# -*- coding: utf-8 -*-

"""Top-level package for openwrt-luci-rpc."""

__author__ = """Finbarr Brady"""
__email__ = 'fbradyirl@github.io'
__version__ = '0.1.0'

from .openwrt_luci_rpc import OpenWrtLuciRPC
from .constants import OpenWrtConstants

class OpenWrtRpc:
    """
    Class to interact with OpenWrt router running luci-mod-rpc package.
    """


    def __init__(self, host_url=OpenWrtConstants.DEFAULT_LOCAL_HOST_URL, username=None, password=None):
        """
        Initiate an instance with a default local ip (192.168.1.1)
        :param ip: Ip of the box if you do not want the default one
        :type ip: str
        :return: A OpenWrtLuciRpc Instance
        """
        self.router = OpenWrtLuciRPC(host_url, username, password)
