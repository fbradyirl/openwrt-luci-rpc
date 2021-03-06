#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `openwrt_luci_rpc` package."""


import unittest
from openwrt_luci_rpc.utilities import is_legacy_version
from packaging import version


class TestOpenwrtLuciRPC(unittest.TestCase):
    """Tests for `openwrt_luci_rpc` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_is_legacy_version(self):
        """Test comparing versions works as expected."""

        assert is_legacy_version(version.parse("15.05")) is True
        assert is_legacy_version(version.parse("15.05.1")) is True
        assert is_legacy_version(version.parse("17.01")) is True
        assert is_legacy_version(version.parse("17.01.6")) is True

        assert is_legacy_version(version.parse("18.06")) is False
        assert is_legacy_version(version.parse("18.06.9")) is False
        assert is_legacy_version(version.parse("19.07.7")) is False

        assert is_legacy_version(version.parse("snapshot")) is False
        assert is_legacy_version(version.parse("21.02-snapshot")) is False
