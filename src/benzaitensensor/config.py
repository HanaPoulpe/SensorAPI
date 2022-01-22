"""Default configuration"""
import logging
import typing

import configuration.exceptions


class DefaultConfig:
    """Hardcoded default configuration"""

    __slots__ = ["default_values"]

    def __init__(self, default_logger: logging.Logger | None = None):
        self.default_values = {
            # Logger Setup
            "logger": default_logger or logging.getLogger("bensaitensensord"),
            "logger.level": logging.DEBUG,
            # Base directories
            "application.dir.blueprints": "./blueprints",
        }

    def load(self) -> None:
        """Nothing to load"""
        pass  # pragma: no cover

    def check(self) -> list[configuration.exceptions.ConfigError]:
        """Nothing to check"""
        pass  # pragma: no cover

    def update(self, conf: configuration.Config):
        """
        Do Nothing

        :param conf:
        """
        pass  # pragma: no cover

    def get_parameters(self) -> typing.Mapping[str, typing.Callable[[], typing.Any]]:
        """
        Return a map of parameter names -> function that returns the parameter value

        :return : A mapping of configuration/values
        """

        def __getter(v: str) -> typing.Callable[[], typing.Any]:
            """Creates a getter"""
            return lambda: self.default_values[v]

        return {k: __getter(k) for k in self.default_values.keys()}


class ApplicationConfiguration:
    """benzaitensensord configuration"""

    __instance: typing.Optional["ApplicationConfiguration"] = None

    def __new__(cls, *args, **kwargs):
        """Replaces the instance creation to provide always return the same instance"""
        if not cls.__instance:
            cls.__instance = super(ApplicationConfiguration, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        self.getters: dict[str, typing.Callable[[], typing.Any]] = dict()
        self.update(DefaultConfig())

    def update(self, conf: configuration.Config):
        """
        Updates configuration getters

        :param conf: Update configuration getters
        """
        conf.load()
        self.getters.update({k: v for k, v in conf.get_parameters().items()})

    def get(self, item: str) -> typing.Any:
        """
        Get a configuration value from its name

        :param item: Parameter name
        :return: parameter value
        """
        return self.getters.get(item, lambda: None)()
