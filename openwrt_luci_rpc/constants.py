class OpenWrtConstants:

    DEFAULT_LOCAL_HOST_URL = "http://192.168.1.1"
    DEFAULT_USERNAME = "root"
    DEFAULT_PASSWORD = ""
    DEFAULT_TIMEOUT = 30

    LUCI_RPC_LOGIN_PATH = '{}/cgi-bin/luci/rpc/auth'
    LUCI_RPC_SYS_PATH = '{}/cgi-bin/luci/rpc/sys'
    LUCI_RPC_UCI_PATH = '{}/cgi-bin/luci/rpc/uci'

    # Only available in 18.06+
    LUCI_RPC_IP_PATH = '{}/cgi-bin/luci/rpc/ip'

    # Make old and new keys consistent for 17 & 18 releases
    # Spaces and dots are removed so keep them out of here also.
    MODERN_KEYS = {
        "HW_address": "mac",
        "IP_address": "ip",
        "dest": "ip"
    }

    def __init__(self):
        pass
