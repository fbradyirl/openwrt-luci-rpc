
import logging
import sys, os

root = logging.getLogger()
root.setLevel(logging.DEBUG)
log = logging.getLogger(__name__)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
root.addHandler(handler)

from openwrt_luci_rpc import OpenWrtRpc

env_name_ip_address = "OPENWRT_IP"
env_name_password = "OPENWRT_PASSWORD"

if not os.getenv(env_name_ip_address):
    log.error("You need to set the router ip environment variable. e.g. ")
    log.error("export {}=<YOUR_ROUTER_IP>".format(env_name_ip_address))
    exit(1)


if not os.getenv(env_name_password):
    log.error("You need to set the router password environment variable. e.g. ")
    log.error("export {}=<YOUR_ROUTER_PASS>".format(env_name_password))
    exit(1)


print('test valid')
r = OpenWrtRpc(os.getenv(env_name_ip_address), 'root', os.getenv(env_name_password), False)

# print('test invalid')
# r = OpenWrtRpc()


r.get_all_connected_devices(only_reachable=False)

#import ipdb
#ipdb.set_trace()
#
# r.get_all_connected_devices(only_reachable=False)
#
# import ipdb
# ipdb.set_trace()
#
# r.get_all_connected_devices(only_reachable=False)
#
# import ipdb
# ipdb.set_trace()
