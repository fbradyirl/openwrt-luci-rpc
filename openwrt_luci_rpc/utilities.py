from .constants import Constants
from packaging import version
import logging

log = logging.getLogger(__name__)


def normalise_keys(result):
    """Replace 17.06 keys with newer ones."""
    if result is not None:

        # named tuple keys cannot have spaces or begin with dots. Replace
        # those with underscores
        result = \
            {k.replace(".", "_").replace(" ", "_"): v for k, v in result.items()}  # noqa: E501

        for old_key, new_key in Constants.MODERN_KEYS.items():
            if old_key in result:
                result[new_key] = result[old_key]
                del result[old_key]

    return result


def get_hostname_from_dhcp(dhcp_result, mac):
    """Determine the hostname for this mac."""
    if isinstance(dhcp_result, dict):
        sections = dhcp_result.values()
    elif isinstance(dhcp_result, list):
        sections = dhcp_result
    else:
        return None

    for section in sections:
        if (not isinstance(section, dict)
                or section.get('.type') != 'host'
                or 'mac' not in section
                or 'name' not in section):
            continue
        if str(mac).upper() in str(section['mac']).upper():
            log.debug("DNS name lookup for mac {} found {}".format(
                mac, section['name']))
            return section['name']

    return None


def is_legacy_version(owrt_version):
    return (
        "snapshot" not in owrt_version.public and
        version.parse("18.06") > owrt_version >= version.parse("15.06")
    )
