"""Environment variable configuration"""
import abc
import dataclasses
import os
import typing

from ..exceptions import ConfigError


@dataclasses.dataclass(frozen=True)
class EnvConfig(abc.ABC):
    """Basic environment config"""

    variable_map: dict[
        str,
        typing.Tuple[str, typing.Callable[[str], typing.Callable[[], typing.Any]]],
    ] = dataclasses.field(default_factory=dict)

    def load(self):
        """Nothing to preload for this class"""
        return

    def check(self) -> typing.List[ConfigError]:
        """
        Check if the parameters are valid

        :return: A comprehensive list of exception from environment
        """
        return_value = []
        for _, (n, f) in self.variable_map.items():
            env = os.getenv(n)
            if not env:
                return_value.append(
                    ConfigError(
                        f"Missing environment variable: {n!r}",
                        level=ConfigError.INFO,
                    ),
                )
                continue

            try:
                f(env)()
            except Exception as err:
                return_value.append(
                    ConfigError(
                        f"Exception creating parameter value for {n!r}={env!r}: {err!r}",
                        level=ConfigError.CRITICAL,
                    ),
                )

        return return_value

    def get_parameters(self) -> typing.Mapping[str, typing.Callable[[], typing.Any]]:
        """
        Return a map of parameter name => callable to create the values

        :return: A mapping of configuration/values
        """
        try:
            return {
                k: f(os.getenv(n))  # type: ignore
                for k, (n, f) in self.variable_map.items()
                if os.getenv(n)
            }
        except Exception as err:
            raise ConfigError(
                f"Exception parsing value from environ {err!r}",
                ConfigError.CRITICAL,
            )
