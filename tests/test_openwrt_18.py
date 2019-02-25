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
        """Test replacing v18 keys works as expected."""

        data = {'dest': "10.1.1.11"}

        data = utilities.normalise_keys(data)

        assert data[Constants.MODERN_KEYS["dest"]] == '10.1.1.11'
