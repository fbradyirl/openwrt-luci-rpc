
|        | Status           |
| ------------- |:-------------:|
| pypi      | [![openwrt_luci_rpc](https://img.shields.io/pypi/v/openwrt_luci_rpc.svg)](https://travis-ci.org/fbradyirl/openwrt-luci-rpc/) |
| travis    | [![Build Status](https://img.shields.io/travis/fbradyirl/openwrt-luci-rpc.svg)](https://travis-ci.org/fbradyirl/openwrt-luci-rpc/)      |
| docs |  [![Build Status](https://readthedocs.org/projects/openwrt-luci-rpc/badge/?version=latest)](https://openwrt-luci-rpc.readthedocs.io/en/latest/?badge=latest)    |


Python3 module for interacting with the OpenWRT Luci RPC interface


* Free software: Apache Software License 2.0
* Documentation: https://openwrt-luci-rpc.readthedocs.io.


Features
--------

* Allows you to use the Luci RPC interface to fetch connected devices on your OpenWrt based router.
* Supports 17.X & 18.X or newer releases of OpenWrt.


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

### Development

See [contributing guide](CONTRIBUTING.rst).
