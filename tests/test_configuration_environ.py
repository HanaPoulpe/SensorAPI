import functools
import os
import unittest

import src.configuration.config_plugins.environ as conf_env


def mock_getenv(_fnc=None, new_env: dict[str, str] | None = None):
    def dec(fnc):
        @functools.wraps(fnc)
        def wrapper(*args, **kwargs):
            _getenv = os.getenv
            os.getenv = new_env.get
            fnc(*args, **kwargs)
            os.getenv = _getenv

        return wrapper

    if not _fnc:
        return dec
    return dec(_fnc)


class TestEnvironConfig(unittest.TestCase):
    def test_load(self):
        env = conf_env.EnvConfig({})
        env.load()
        self.assertTrue(True, "EnvConfig - Load")

    @mock_getenv(new_env={"ENV_VALUE": "value"})
    def test_check_no_issue(self):
        env = conf_env.EnvConfig(
            {
                "value": ("ENV_VALUE", lambda x: lambda: x),
            }
        )
        errors = env.check()

        self.assertListEqual([], errors)

    @mock_getenv(new_env={"ENV_VALUE": "value"})
    def test_check_missing(self):
        env = conf_env.EnvConfig(
            {
                "value": ("ENV_VALUE", lambda x: lambda: x),
                "missing": ("MISSING", lambda x: lambda: x),
            }
        )
        errors = env.check()

        self.assertEqual(1, len(errors))
        self.assertEqual(errors[0].level, conf_env.ConfigError.INFO[0])

    @mock_getenv(new_env={"ENV_VALUE": "value"})
    def test_check_error(self):
        def fail(v: str):
            raise Exception()

        env = conf_env.EnvConfig({"failing": ("ENV_VALUE", fail)})
        errors = env.check()

        self.assertEqual(1, len(errors))
        self.assertEqual(errors[0].level, conf_env.ConfigError.CRITICAL[0])

    @mock_getenv(new_env={"ENV_VALUE": "value"})
    def test_get_parameter_no_issue(self):
        env = conf_env.EnvConfig(
            {
                "param": ("ENV_VALUE", lambda x: lambda: x),
            }
        )
        params = env.get_parameters()

        self.assertIn("param", params)
        self.assertEqual(params["param"](), "value")

    @mock_getenv(new_env={"ENV_VALUE": "value"})
    def test_get_parameter_missing(self):
        env = conf_env.EnvConfig(
            {
                "param": ("ENV_VALUE", lambda x: lambda: x),
                "missing": ("MISSING", lambda x: lambda: x),
            }
        )
        params = env.get_parameters()

        self.assertIn("param", params)
        self.assertEqual(params["param"](), "value")

    @mock_getenv(new_env={"ENV_VALUE": "value"})
    def test_get_parameter_error(self):
        def fail(v: str):
            raise Exception()

        env = conf_env.EnvConfig({"failing": ("ENV_VALUE", fail)})
        self.assertRaises(conf_env.ConfigError, env.get_parameters)
