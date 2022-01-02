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

    def get(self, item: str) -> typing.Any:
        """
        Returns item value

        :param item: item name
        :type item: str
        :return: any
        """
        ...
