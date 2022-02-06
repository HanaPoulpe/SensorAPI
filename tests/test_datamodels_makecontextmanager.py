"""Test MakeContextManager decorator"""
import unittest

import src.benzaitensensor.datamodels as datamodels


@datamodels.MakeContextManager()
class MockInterface:
    class Cursor:
        def __init__(self):
            self.close_count = 0
            self.side_effect = None

        def read(self, keys, cls):
            if self.side_effect:
                raise self.side_effect
            return []

        def write(self, data, no_wait):
            pass

        def write_many(self, datas, no_wait):
            pass

        def close(self):
            self.close_count += 1

    def __init__(self):
        self.cursor = self.Cursor()
        self.connect_count = 0
        self.close_count = 0

    def setup(self, *args, **kwargs):
        pass

    def connect(self):
        self.connect_count += 1
        return self.cursor

    def close(self):
        self.close_count += 1


class MockDataObject:
    def to_item_map(self):
        return dict

    @classmethod
    def attributes(cls):
        return dict(), dict()

    @classmethod
    def get_data_interface_params(cls):
        pass


class TestMakeContextManager(unittest.TestCase):
    def setUp(self) -> None:
        """Reset the mock interface"""
        self.interface = MockInterface()

    def test_enter_exit_no_issue(self):
        """
        Attempt to enter in Interface context before closing it.

        Expected behavior is:
        Interface.connect == 1
        Interface.close == 1
        Cursor.close == 1
        """
        with self.interface as cur:
            self.assertIsInstance(
                cur,
                MockInterface.Cursor,  # type: ignore
                "cur is not the expected type",
            )

        self.assertEqual(self.interface.connect_count, 1)  # type: ignore
        self.assertEqual(self.interface.close_count, 1)  # type: ignore
        self.assertEqual(self.interface.cursor.close_count, 1)  # type: ignore

    def test_enter_except(self):
        """
        Attempt to enter the Interface context, raise an exception from the context

        Expected behavior is:
        Interface.connect == 1
        Interface.close == 1
        Cursor.close == 1
        """
        def context_runner(interface):
            with interface as cur:
                cur.read({"test": "val"}, MockDataObject)  # type: ignore

        class TestError(Exception):
            pass

        self.interface.cursor.side_effect = TestError()  # type: ignore
        self.assertRaises(TestError, context_runner, self.interface)

        self.assertEqual(self.interface.connect_count, 1)  # type: ignore
        self.assertEqual(self.interface.close_count, 1)  # type: ignore
        self.assertEqual(self.interface.cursor.close_count, 1)  # type: ignore


class TestMakeContextManagerInvalidClass(unittest.TestCase):
    def test_make_context_manager_fail(self):
        def test():
            @datamodels.MakeContextManager()
            class T:
                pass

        self.assertRaises(TypeError, test)


if __name__ == "__main__":
    unittest.main()
