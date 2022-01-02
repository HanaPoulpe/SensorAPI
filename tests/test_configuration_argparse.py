import sys
import unittest

import src.configuration.config_plugins.argparse as conf_argparse


class TestArgumentParserConfig(unittest.TestCase):
    def test_load_no_arg_list(self):
        sysargv = sys.argv
        sys.argv = ["test", "--foo", "foo"]
        try:
            parser = conf_argparse.ArgumentParser(exit_on_error=False)
            parser.add_argument("--foo")

            config_parser = conf_argparse.ArgumentParserConfig(parser)
            config_parser.load()
            self.assertTrue(True, "ArgumentParserConfig - no arg list")
        except Exception as e:
            raise e
        finally:
            sys.argv = sysargv

    def test_load_arg_list(self):
        argv = ["--foo", "foo"]
        parser = conf_argparse.ArgumentParser(exit_on_error=False)
        parser.add_argument("--foo")

        config_parser = conf_argparse.ArgumentParserConfig(parser, argv)
        config_parser.load()
        self.assertTrue(True, "ArgumentParserConfig - arg list")

    def test_load_argument_error(self):
        argv = ["--foo", "foo"]
        parser = conf_argparse.ArgumentParser(exit_on_error=False)
        parser.add_argument("--bar")

        config_parser = conf_argparse.ArgumentParserConfig(parser, argv)
        self.assertRaises(conf_argparse.ConfigError, config_parser.load)

    def test_check_no_error(self):
        argv = ["--foo", "foo"]
        parser = conf_argparse.ArgumentParser(exit_on_error=False)
        parser.add_argument("--foo")

        config_parser = conf_argparse.ArgumentParserConfig(parser, argv)
        self.assertListEqual(config_parser.check(), [])

    def test_check_error(self):
        argv = ["--foo", "foo"]
        parser = conf_argparse.ArgumentParser(exit_on_error=False)
        parser.add_argument("--bar")

        config_parser = conf_argparse.ArgumentParserConfig(parser, argv)
        check = config_parser.check()
        self.assertEqual(len(check), 1)
        self.assertIsInstance(check[0], conf_argparse.ConfigError)

    def test_get_parameters_preloaded(self):
        argv = ["--foo", "foo"]
        parser = conf_argparse.ArgumentParser(exit_on_error=False)
        parser.add_argument("--foo")

        config_parser = conf_argparse.ArgumentParserConfig(parser, argv)
        config_parser.load()

        params = config_parser.get_parameters()

        self.assertIn("foo", params)
        self.assertEqual(params["foo"](), "foo")

    def test_get_parameters_no_load(self):
        argv = ["--foo", "foo"]
        parser = conf_argparse.ArgumentParser(exit_on_error=False)
        parser.add_argument("--foo")

        config_parser = conf_argparse.ArgumentParserConfig(parser, argv)
        params = config_parser.get_parameters()

        self.assertIn("foo", params)
        self.assertEqual(params["foo"](), "foo")


if __name__ == "__main__":
    unittest.main()
