__author__ = 'Andrey'

import unittest
from SCE_Nimrod import find_redundant_points
from test_determine_enclosure_centre_side import get_default_points


class MyTestCase(unittest.TestCase):
    def test_something(self):
        p = get_default_points()
        rejected = find_redundant_points(p)
        self.assertTrue(len(rejected) == 1)
        self.assertTrue(rejected[0].get_x() == -1.0)
        self.assertTrue(rejected[0].get_y() == 1.0)


if __name__ == '__main__':
    unittest.main()
