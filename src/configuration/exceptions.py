"""Config Exceptions"""
import typing


class ConfigError(Exception):
    """Basic Config Exception"""

    INFO = (0, "INFO")
    WARNING = (1, "WARNING")
    DEPRECATED = (2, "DEPRECATED")
    RECOVERED = (10, "RECOVERED ERROR")
    ERROR = (50, "ERROR")
    CRITICAL = (100, "CRITICAL ERROR")

    def __init__(
        self,
        msg: str,
        level: typing.Tuple[int, str],
        *args,
    ):  # pragma: no cover
        """
        Basic configuration error

        :param msg: Error message
        :type msg: str
        :param level: Error level
        :type level: Tuple[int, str] (level, name)
        :param *args: Positional arguments for Exception super class
        """
        super(ConfigError, self).__init__(msg, *args)
        self.msg = msg
        self.level = level[0]
        self.level_name = level[1]

    def __str__(self) -> str:
        return self.msg

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}::{self.level_name}::{self.msg}"
