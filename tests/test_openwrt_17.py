#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `openwrt_luci_rpc` package."""


import unittest
from openwrt_luci_rpc import utilities
from openwrt_luci_rpc.constants import Constants


class TestOpenwrtLuciRPC(unittest.TestCase):
    """Tests for `openwrt_luci_rpc` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_normalise_keys(self):
        """Test replacing v17 keys works as expected."""

        data = {
                "HW type": "0x1",
                "Mask": "*",
                "Flags": "0x2",
                "Device": "br-lan",
                'HW address': '9C:20:7B:CA:A2:16',
                'IP address': "127.0.0.1",
                }

        data = utilities.normalise_keys(data)

        assert data[Constants.MODERN_KEYS["HW_address"]] == '9C:20:7B:CA:A2:16'
        assert data[Constants.MODERN_KEYS["IP_address"]] == '127.0.0.1'
        assert data['HW_type'] == "0x1"
        assert data['Mask'] == "*"
        assert data['Flags'] == "0x2"
        assert data['Device'] == "br-lan"
