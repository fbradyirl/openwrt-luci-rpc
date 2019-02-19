================
openwrt-luci-rpc
================


.. image:: https://img.shields.io/pypi/v/openwrt_luci_rpc.svg
        :target: https://pypi.python.org/pypi/openwrt_luci_rpc

.. image:: https://img.shields.io/travis/fbradyirl/openwrt-luci-rpc.svg
        :target: https://travis-ci.org/fbradyirl/openwrt-luci-rpc/

.. image:: https://readthedocs.org/projects/openwrt-luci-rpc/badge/?version=latest
        :target: https://openwrt-luci-rpc.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Module for interacting with OpenWRT Luci RPC interface


* Free software: Apache Software License 2.0
* Documentation: https://openwrt-luci-rpc.readthedocs.io.


Features
--------

* TODO


Usage
--------

You will first need to install the package `luci-mod-rpc` on your OpenWrt router.

```
opkg update
opkg install luci-mod-rpc
```

Once that is done, you can use this module to interact with the RPC interface.


### Install

```bash
pip install openwrt-luci-rpc
```

### Use

```python
from openwrt_luci_rpc import OpenWrtRpc

router = OpenWrtRpc('http://192.168.1.1', 'root', 'mypassword')

```
