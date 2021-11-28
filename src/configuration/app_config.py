"""Server configuration handler"""
import typing

from .config import Config


class AppConfig(typing.Protocol):
    """Default application configuration"""

    def update(self, conf: Config) -> None:
        """
        Updates current configuration

        :param conf: Configuration set
        """
        ...
