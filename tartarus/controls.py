"""Defensive controls for synthetic scenarios."""

from ipaddress import ip_address


def web_headers(headers):
    normalized = {name.lower(): value.strip().lower() for name, value in headers.items()}
    return len(normalized) == len(headers) and (
        normalized.get("x-content-type-options") == "nosniff"
        and normalized.get("x-frame-options") == "deny"
    )


def api_contract(record):
    return (
        isinstance(record, dict)
        and set(record) == {"name", "enabled"}
        and isinstance(record["name"], str)
        and 1 <= len(record["name"].strip()) <= 80
        and type(record["enabled"]) is bool
    )


def local_listeners(addresses):
    try:
        return bool(addresses) and all(ip_address(address).is_loopback for address in addresses)
    except ValueError:
        return False


def container_policy(config):
    # This is a projected inventory, not a Compose parser.
    return (
        config["privileged"] is False
        and type(config["uid"]) is int
        and config["uid"] > 0
        and config["host_mounts"] == []
        and config["added_capabilities"] == []
        and type(config["memory_mib"]) is int
        and 1 <= config["memory_mib"] <= 512
    )


def connection_limit(value):
    return type(value) is int and 1 <= value <= 1000


CONTROLS = {
    "TAR-001": web_headers,
    "TAR-002": api_contract,
    "TAR-003": local_listeners,
    "TAR-004": container_policy,
    "TAR-007": connection_limit,
}
