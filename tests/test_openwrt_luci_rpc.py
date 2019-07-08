#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `openwrt_luci_rpc` package."""


import unittest
from unittest.mock import Mock, patch

from openwrt_luci_rpc import OpenWrtRpc
from openwrt_luci_rpc.constants import Constants
from openwrt_luci_rpc import utilities
from openwrt_luci_rpc.exceptions import LuciConfigError


class TestOpenwrtLuciRPC(unittest.TestCase):
    """Tests for `openwrt_luci_rpc` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_none_host(self):
        """Test invalid host raises exception."""
        with self.assertRaises(LuciConfigError):
            OpenWrtRpc(None)

    def test_empty_host(self):
        """Test invalid host raises exception."""
        with self.assertRaises(LuciConfigError):
            OpenWrtRpc("")

    @patch('requests.Session.post')
    def test_defaults(self, mock_post):
        """Test defaults are in place."""

        json_result = {
            "id": "1",
            "result": "2e9f2c44d34a10e1321de7893123123221",
            "error": None
        }

        mock_post.return_value = Mock(ok=True)
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = json_result

        runner = OpenWrtRpc()
        assert runner.router.host_api_url == '{}://{}'.format("http", Constants.DEFAULT_LOCAL_HOST)
        assert runner.router.username == Constants.DEFAULT_USERNAME
        assert runner.router.password == Constants.DEFAULT_PASSWORD

    def test_normalise_key_stripping(self):
        """Test replacing dots and spaces works."""

        data = {
            ".name": "cfg07ee1",
            ".type": "host",
            "name": "imac-ethernet",
            ".index": 4,
            "mac": "c8:2a:10:4a:10:dd",
            "dns": "1",
            ".anonymous": True,
            "ip": "192.168.1.124"
        }

        data = utilities.normalise_keys(data)

        assert data['_name'] == "cfg07ee1"
        assert data['_type'] == "host"
        assert data['ip'] == "192.168.1.124"
