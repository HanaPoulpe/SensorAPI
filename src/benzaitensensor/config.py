"""Default configuration"""
import logging
import typing

import configuration
import configuration.exceptions


class DefaultConfig:
    """Hardcoded default configuration"""

    __slots__ = ["default_values"]

    def __init__(self):
        self.default_values = {
            # Logger Setup
            "logger": logging.getLogger("bensaitensensord"),
            "logger.level": logging.DEBUG,
            # Base directories
            "application.dir.blueprints": "./blueprints",
        }

    def load(self) -> None:
        """Nothing to load"""
        pass

    def check(self) -> list[configuration.exceptions.ConfigError]:
        """Nothing to check"""
        pass

    def update(self, conf: configuration.Config):
        """
        Do Nothing

        :param conf:
        """
        pass

    def get_parameters(self) -> typing.Mapping[str, typing.Callable[[], typing.Any]]:
        """
        Return a map of parameter names -> function that returns the parameter value

        :return : A mapping of configuration/values
        """
        return {k: lambda: v for k, v in self.default_values.items()}


class ApplicationConfiguration:
    """benzaitensensord configuration"""

    __instance: typing.Optional["ApplicationConfiguration"] = None

    @classmethod
    def get_instance(cls):
        """Returns the Application configuration"""
        if not cls.__instance:
            cls()
        return cls.__instance

    @classmethod
    def __set_instance(cls, instance: "ApplicationConfiguration"):
        """Sets the application instance if not set"""
        if not cls.__instance:
            cls.__instance = instance

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            return cls.__init__(*args, **kwargs)
        return cls.__instance

    def __init__(self):
        self.__set_instance(self)

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
        Return
        :param item: Parameter name
        :return: parameter value
        """
        return self.__dict__.get(item, lambda: None)()
