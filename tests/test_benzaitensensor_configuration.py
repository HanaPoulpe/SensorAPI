"""Unit tests for application config"""
import unittest

from src.benzaitensensor.config import *


class TestApplicationConfiguration(unittest.TestCase):
    """Tests global app configuration"""

    def test_new(self):
        """
        Instantiating an instance of ApplicationConfiguration should always return the
        same instance
        """
        first_config = ApplicationConfiguration()
        second_config = ApplicationConfiguration()

        self.assertIs(first_config, second_config)

    def test_default_config(self):
        """
        Check type and presence of every configuration required for the application to
        work
        """
        conf = ApplicationConfiguration()

        self.assertIsInstance(conf.get("logger"), logging.Logger)
        self.assertEqual(conf.get("logger.level"), logging.DEBUG)

        self.assertIn("/blueprints", conf.get("application.dir.blueprints"))

        self.assertIsNone(conf.get("x-test-missing-key-x"))


if __name__ == "__main__":
    unittest.main()
