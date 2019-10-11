#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `openwrt_luci_rpc` package."""

import unittest
import os
from openwrt_luci_rpc.openwrt_luci_rpc import OpenWrtLuciRPC


class TestOpenwrt15LuciRPC(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    @unittest.skip("unskip this to test using env vars")
    def testDiscover(self):
        # HOST, USER, PASSWORD,[HTTPS] must be in env variables in order
        # to run the test
        assert "HOST" in os.environ
        assert "USER" in os.environ
        assert "PASSWORD" in os.environ

        router = OpenWrtLuciRPC(
                    os.getenv("HOST"),
                    os.getenv("USER"),
                    os.getenv("PASSWORD"),
                    os.getenv("HTTPS", "False") == "True",
                    os.getenv("VERIFY_HTTPS", "False") == "True",
                )
        devices = router.get_all_connected_devices(False, False)
        assert devices is not None


if __name__ == '__main__':
    unittest.main()
