"""Register for all data interfaces"""
from .data_interfaces import DataInterface


class _Register:
    """
    This class is only there to maintain the register.

    It's a super lightweight singleton as it should not be accessed outside of this module.
    It basically maintain a database name -> DataInterface list.
    """

    instance = None

    def __init__(self, default_interface: DataInterface):
        _Register.instance = self
        self.register: dict[str, DataInterface] = dict()
        self.default = default_interface

    @classmethod
    def get_instance(cls) -> "_Register":
        """Return Register instance"""
        return _Register.instance


def register_data_interface(name: str, interface: DataInterface, set_default: bool = False):
    """
    Register or overwrite a data interface.

    If no default interface is set, the first interface register is the default.

    :param name: Name of the Register
    :param interface: DataInterface instance to register
    :param set_default: Replace default value
    """
    register = _Register.get_instance() or _Register(interface)
    register.register[name] = interface
    if set_default:
        register.default = interface


def get_data_interface(name: str) -> DataInterface | None:
    """
    Returns a database interface to matching the name or the default interface.

    When no interface is set, returns None
    """
    register = _Register.get_instance()
    if not register:
        return None

    return register.register.get(name, register.default)
