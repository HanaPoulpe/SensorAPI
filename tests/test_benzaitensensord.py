import unittest


import src.benzaitensensor.benzaitensensord as benzaitensensord

class BenzaitenSensorDTest(unittest.TestCase):
    def test_root(self):
        response = benzaitensensord.hello_world()
        self.assertEqual(response, "Hello World!")


if __name__ == "__main__":
    unittest.main()