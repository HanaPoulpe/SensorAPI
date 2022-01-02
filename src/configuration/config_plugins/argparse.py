"""Command line parameter implementation"""
import argparse
import typing

from ..exceptions import ConfigError


class ArgumentParser(argparse.ArgumentParser):
    """ArgumentParser but don't exit on error"""

    def error(self, message: str):
        """Raises a ConfigError"""
        raise ConfigError(
            message,
            ConfigError.CRITICAL,
        )


class ArgumentParserConfig:
    """Wraps argparse ArgumentParser for Config protocol"""

    def __init__(
        self,
        parser: ArgumentParser,
        arg_list: typing.Optional[list] = None,
    ):
        """
        Create a ArgumentParserConfig

        :param parser: argument parser
        :param arg_list: list of argument, default will be argparse default.
        """
        self.parser = parser
        self.arg_list = arg_list
        self.args: typing.Optional[argparse.Namespace] = None

    def load(self) -> None:
        """Parse argument list"""
        if self.arg_list is None:
            self.args = self.parser.parse_args()
        else:
            self.args = self.parser.parse_args(self.arg_list)

    def check(self) -> typing.List[ConfigError]:
        """
        Checks if the configuration is valid

        :return: List of exceptions
        """
        try:
            self.load()
        except ConfigError as err:
            return [err]

        return list()

    def get_parameters(self) -> typing.Mapping[str, typing.Callable[[], typing.Any]]:
        """Return a list of parameters name -> function that return their value"""
        if not self.args:
            self.load()

        def wrap(x) -> typing.Callable:
            """
            Wrap a value to a callable to this value

            :param x: any value
            :return: func() -> x
            """
            return lambda: x

        return {k: wrap(v) for k, v in self.args.__dict__.items()}
