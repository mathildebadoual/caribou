import caribou.clock as clock
import unittest

class TestContructionTimer(unittest.TestCase):
    def setUp(self):
        self.clock = clock.Timer()

    def test_get_time(self):
        self.clock.set_next_time_step(3600*2)
        self.assertEqual(self.clock.get_time(type_time='h'), 2)

if __name__ == '__main__':
    unittest.main()
