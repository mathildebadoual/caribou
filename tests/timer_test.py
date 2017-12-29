import caribou.timer as timer
import unittest

class TestContructionTimer(unittest.TestCase):
    def setUp(self):
        self.timer = timer.Timer()

    def test_get_time(self):
        self.timer.set_next_time_step(3600*2)
        self.assertEqual(self.timer.get_time(type_time='h'), 2)

if __name__ == '__main__':
    unittest.main()
