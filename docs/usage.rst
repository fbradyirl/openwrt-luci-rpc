=====
Usage
=====

To use openwrt-luci-rpc in a project,
you will first need to install the package ``luci-mod-rpc`` on your
OpenWrt router.

::

   opkg update
   opkg install luci-mod-rpc

Once that is done, you can use this module to interact with the RPC
interface.


.. code:: python

   from openwrt_luci_rpc import OpenWrtRpc

   router = OpenWrtRpc('192.168.1.1', 'root', 'mypassword')
   result = router.get_all_connected_devices(only_reachable=True)

   for device in result:
      mac = device.mac
      name = device.hostname

      # convert class to a dict
      device_dict = device._asdict()
