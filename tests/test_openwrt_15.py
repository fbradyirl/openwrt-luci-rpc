#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `openwrt_luci_rpc` package."""

import unittest
import config
from openwrt_luci_rpc.openwrt_luci_rpc import utilities, OpenWrtLuciRPC
from openwrt_luci_rpc.constants import Constants

class TestOpenwrt15LuciRPC(unittest.TestCase):
    def testLogin(self):
        device = OpenWrtLuciRPC(config.host, config.username, config.password, config.is_https)


if __name__ == '__main__':
    unittest.main()