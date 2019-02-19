#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `openwrt_luci_rpc` package."""


import unittest
import requests

from openwrt_luci_rpc import OpenWrtRpc
# from openwrt_luci_rpc.constants import OpenWrtConstants


class TestOpenwrtLuciRPC(unittest.TestCase):
    """Tests for `openwrt_luci_rpc` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_none_host(self):
        """Test invalid host raises exception."""
        with self.assertRaises(requests.exceptions.MissingSchema):
            OpenWrtRpc(None)

    def test_empty_host(self):
        """Test invalid host raises exception."""
        with self.assertRaises(requests.exceptions.MissingSchema):
            OpenWrtRpc("")

    def test_no_schema_host(self):
        """Test invalid host raises exception."""
        with self.assertRaises(requests.exceptions.MissingSchema):
            OpenWrtRpc("192.168.1.1")

    # def test_defaults(self):
    #     """Test defaults are in place."""
    #     runner = OpenWrtRpc()
    #     assert runner.router.username == OpenWrtConstants.DEFAULT_USERNAME
