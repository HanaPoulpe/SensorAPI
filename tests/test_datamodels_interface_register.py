"""Tests datamodels.interface register"""
import importlib
import unittest

import src.benzaitensensor.datamodels as datamodels
import src.benzaitensensor.datamodels.interfaces_register as target


@datamodels.MakeContextManager()
class MockInterface:
    class Cursor:
        def read(self, keys, cls):
            return []

        def write(self, data, no_wait):
            pass

        def write_many(self, datas, no_wait):
            pass

        def close(self):
            pass

    def setup(self, *args, **kwargs):
        pass

    def connect(self):
        return self.Cursor()

    def close(self):
        pass


class TestRegisterDataInterface(unittest.TestCase):
    def test_register_no_set_default(self):
        """Test the case where default interface is not forced"""
        interface = MockInterface()
        datamodels.register_data_interface(self.__class__.__name__, interface)

        self.assertTrue(True, __name__)

    def test_register_set_default(self):
        """Test the case where the default interface is forced"""
        interface = MockInterface()
        datamodels.register_data_interface(self.__class__.__name__, interface, True)

        self.assertTrue(True, __name__)


class TestGetDataInterfaceNoInterfaces(unittest.TestCase):
    def setUp(self) -> None:
        """Forces target module reload to reset the register"""
        importlib.reload(target)

    def test_not_interfaces_registered(self):
        """
        Try to get a data interface before any was registered.

        The method should return None
        """
        interface = datamodels.get_data_interface(self.__class__.__name__)

        self.assertIsNone(interface, "Interface should not exists")


class TestGetDataInterface(unittest.TestCase):
    def setUp(self) -> None:
        """Ensures only 2 interfaces are registered"""
        importlib.reload(target)

        self.interface1 = MockInterface()
        self.interface2 = MockInterface()

        datamodels.register_data_interface("interface1", self.interface1, True)
        datamodels.register_data_interface("interface2", self.interface2)

    def test_get_interface1(self):
        """Interface register as interface1 should be the same object as self.interface1"""
        interface = datamodels.get_data_interface("interface1")

        self.assertIs(interface, self.interface1)

    def test_get_interface2(self):
        """Interface register as interface2 should be the same object as self.interface2"""
        interface = datamodels.get_data_interface("interface2")

        self.assertIs(interface, self.interface2)

    def test_get_default(self):
        """Not interface named default exist, getting it should return self.interface1"""
        interface = datamodels.get_data_interface("default")

        self.assertIs(interface, self.interface1)


if __name__ == "__main__":
    unittest.main()
