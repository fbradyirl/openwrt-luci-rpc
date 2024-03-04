#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `openwrt_luci_rpc` package."""


import unittest

from openwrt_luci_rpc import utilities


class TestOpenwrtLuciRPC(unittest.TestCase):
    """Tests for `openwrt_luci_rpc` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_get_hostname_from_dhcp_mac_list_formating(self):
        """Test if lower case list of MAC match with Upper case."""

        data = [
            {
                ".name": "cfg07ee1",
                ".type": "host",
                "name": "imac-ethernet",
                ".index": 4,
                "mac": ["c8:2a:10:4a:10:dd"],
                "dns": "1",
                ".anonymous": True,
                "ip": "192.168.1.124",
            }
        ]

        data = utilities.get_hostname_from_dhcp(data, "C8:2A:10:4A:10:DD")
        assert data is None

    def test_get_hostname_from_dhcp_mac_string_formating(self):
        """Test if lower case string of MAC match with Upper case."""

        data = [
            {
                ".name": "cfg07ee1",
                ".type": "host",
                "name": "imac-ethernet",
                ".index": 4,
                "mac": "c8:2a:10:4a:10:dd",
                "dns": "1",
                ".anonymous": True,
                "ip": "192.168.1.124",
            }
        ]

        data = utilities.get_hostname_from_dhcp(data, "C8:2A:10:4A:10:DD")
        assert data is None

    def test_get_hostname_from_dhcp_multiple_mac_string_formating(self):
        """Test if lower case string of MAC match with Upper case of multi mac list."""  # noqa: E501python setup.py test

        data = [
            {
                ".name": "cfg07ee1",
                ".type": "host",
                "name": "imac-ethernet",
                ".index": 4,
                "mac": {"c8:2a:10:4a:10:d9", "c8:2a:10:4a:10:dd"},
                "dns": "1",
                ".anonymous": True,
                "ip": "192.168.1.124",
            }
        ]

        data = utilities.get_hostname_from_dhcp(data, "C8:2A:10:4A:10:DD")
        assert data is None
        data = utilities.get_hostname_from_dhcp(data, "C8:2A:10:4A:10:D9")
        assert data is None
