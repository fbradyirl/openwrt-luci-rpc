#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `openwrt_luci_rpc` package."""

import unittest
import config
from openwrt_luci_rpc.openwrt_luci_rpc import OpenWrtLuciRPC


class TestOpenwrt15LuciRPC(unittest.TestCase):

    def testDiscover(self):
        router = OpenWrtLuciRPC(config.host, config.username,
                                config.password, config.is_https)

        devices = router.get_all_connected_devices(False, False)
        assert devices is not None


if __name__ == '__main__':
    unittest.main()
