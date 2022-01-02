"""Configuration protocol"""
import typing

from .exceptions import ConfigError


class Config(typing.Protocol):
    """Basic configuration reader protocol"""

    def load(self) -> None:
        """Load the configuration"""
        ...

    def check(self) -> typing.List[ConfigError]:
        """
        Check if the configuration is valid

        :return : A comprehensive list of exception from the configuration
        """
        ...

    def get_parameters(self) -> typing.Mapping[str, typing.Callable[[], typing.Any]]:
        """
        Return a map of parameter names -> function that returns the parameter value

        :return : A mapping of configuration/values
        """
        ...
