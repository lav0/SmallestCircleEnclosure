__author__ = 'Andrey'

import unittest
from SCE_Nimrod import find_redundant_points
from SimpleMath import Vector2D
from test_determine_enclosure_centre_side import get_default_points
from test_determine_enclosure_centre_side import get_extra_default_points
from test_reduced_circle import generate_random_points_list
from TimeMeasureDecorator import function_call_log_decorator
from readwrite_list import read_list_of_points
from readwrite_list import write_list_of_points
from SCE_Direct import find_smallest_circle_directly


class MyTestCase(unittest.TestCase):
    @function_call_log_decorator
    def test_something(self):
        p = get_default_points()
        copy = list(p)
        length_before = len(p)
        rejected = find_redundant_points(p)
        self.assertTrue(len(rejected) == 1)
        self.assertTrue(rejected[0].get_x() == -1.0)
        self.assertTrue(rejected[0].get_y() == 1.0)
        for r in rejected:
            p.remove(r)
        self.assertEqual(length_before - 1, len(p))
        rejected = find_redundant_points(p)
        self.assertTrue(len(rejected) == 1)
        self.assertTrue(rejected[0].get_x() == 2.0)
        self.assertTrue(rejected[0].get_y() == 0.0)
        circle_nimrod, dumb = find_smallest_circle_directly(p)
        circle_expect, dumb = find_smallest_circle_directly(copy)
        self.assertEqual(circle_expect.radius, circle_nimrod.radius)
        self.assertEqual(circle_expect.centre.get_x(), circle_nimrod.centre.get_x())
        self.assertEqual(circle_expect.centre.get_y(), circle_nimrod.centre.get_y())

    @function_call_log_decorator
    def test_even_number_of_bisectors(self):
        p = get_extra_default_points()
        self.internal_test(p)

    def internal_test(self, p):
        copy = list(p)
        number_of_points = len(p)
        while number_of_points > 4:
            print number_of_points
            # if number_of_points == 17:
            #     write_list_of_points(p, "Test0.txt")
            rejected = find_redundant_points(p)
            if not rejected:
                assert True
            for r in rejected:
                p.remove(r)
            number_of_points = len(p)
        circle_nimrod, dumb = find_smallest_circle_directly(p)
        circle_expect, dumb = find_smallest_circle_directly(copy)
        self.assertEqual(circle_expect.radius, circle_nimrod.radius)
        self.assertEqual(circle_expect.centre.get_x(), circle_nimrod.centre.get_x())
        self.assertEqual(circle_expect.centre.get_y(), circle_nimrod.centre.get_y())

    @function_call_log_decorator
    def test_from_file(self):
        self.internal_test(read_list_of_points("TestDetermineSide20.txt"))
        #self.internal_test(read_list_of_points("Test0.txt"))

    @function_call_log_decorator
    def test_eight_points_test(self):
        for i in range(2):
            p = generate_random_points_list(8, 20.0)
            rejected = find_redundant_points(p)
            print rejected
            self.assertTrue(rejected)

    @function_call_log_decorator
    def test_1(self):
        p = get_default_points()
        p.append(Vector2D(0.0, 0.0))
        #rejected = find_redundant_points(p)
        #print [p.get_both() for p in rejected]
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
