#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `openwrt_luci_rpc` package."""


import unittest
from unittest.mock import Mock, patch

from openwrt_luci_rpc import OpenWrtRpc
from openwrt_luci_rpc.constants import OpenWrtConstants
from openwrt_luci_rpc.exceptions import InvalidLuciTokenError, \
    LuciRpcMethodNotFoundError, InvalidLuciLoginError, \
    LuciRpcUnknownError, PageNotFoundError

class TestOpenwrtLuciRPC(unittest.TestCase):
    """Tests for `openwrt_luci_rpc` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    @patch('requests.Session.post')
    def test_determine_if_legacy_version(self, mock_post):
        """Test _determine_if_legacy_version for v17"""

        # mock_post.return_value = Mock(ok=True)
        mock_post.side_effect = PageNotFoundError('')  # <- note no brackets,

        runner = OpenWrtRpc()
        assert runner.is_legacy_version == True
