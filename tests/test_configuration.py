import unittest

import src.configuration as configuration
import src.configuration.exceptions as cfg_error


class TestConfigImport(unittest.TestCase):
    def test_import(self):
        self.assertTrue(hasattr(configuration, "AppConfig"), "AppConfig exists")
        self.assertTrue(hasattr(configuration, "Config"), "Config exists")


class TestConfigError(unittest.TestCase):
    def test_str(self):
        e = cfg_error.ConfigError(
            "Testing Error",
            cfg_error.ConfigError.INFO,
        )

        self.assertEqual("Testing Error", str(e))

    def test_repr(self):
        e = cfg_error.ConfigError(
            "Testing Error",
            cfg_error.ConfigError.INFO,
        )

        self.assertEqual("ConfigError::INFO::Testing Error", repr(e))


if __name__ == "__main__":
    unittest.main()
