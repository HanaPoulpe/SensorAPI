"""Manages authentication requests"""


def check_authorized(api_key: str, sensor_id: str, method: str, source: str) -> bool:
    """
    Checks if the request is authorized

    ATM does nothing
    """
    return True
