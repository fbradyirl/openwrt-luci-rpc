#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `openwrt_luci_rpc` package."""


import unittest
import requests
from unittest.mock import Mock, patch

from openwrt_luci_rpc import OpenWrtRpc
from openwrt_luci_rpc.constants import OpenWrtConstants


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
        assert runner.router.host_api_url == OpenWrtConstants.DEFAULT_LOCAL_HOST_URL
        assert runner.router.username == OpenWrtConstants.DEFAULT_USERNAME
        assert runner.router.password == OpenWrtConstants.DEFAULT_PASSWORD
