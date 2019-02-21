from .constants import OpenWrtConstants
import logging

log = logging.getLogger(__name__)


def normalise_keys(result):
    """Replace 17.06 keys with newer ones."""

    for old_key, new_key in OpenWrtConstants.MODERN_KEYS.items():
        if old_key in result:
            result[new_key] = result[old_key]
            del result[old_key]


def get_hostname_from_dhcp(dhcp_result, mac):
    # determine hostname
    if dhcp_result:
        hosts = [x for x in dhcp_result.values()
                 if x['.type'] == 'host' and
                 'mac' in x and 'name' in x]
        mac2name_list = [
            (x['mac'].upper(), x['name']) for x in hosts]
        mac2name = dict(mac2name_list)
        return mac2name.get(mac, None)

    return None
