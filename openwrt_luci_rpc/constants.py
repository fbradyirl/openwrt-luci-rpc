class OpenWrtConstants:

    DEFAULT_LOCAL_HOST_URL = "http://192.168.1.1"
    DEFAULT_USERNAME = "root"
    DEFAULT_PASSWORD = ""
    DEFAULT_TIMEOUT = 30

    LUCI_RPC_LOGIN_PATH = '{}/cgi-bin/luci/rpc/auth'
    LUCI_RPC_SYS_PATH = '{}/cgi-bin/luci/rpc/sys'
    LUCI_RPC_IP_PATH = '{}/cgi-bin/luci/rpc/ip'
    LUCI_RPC_UCI_PATH = '{}/cgi-bin/luci/rpc/uci'

    def __init__(self):
        pass
