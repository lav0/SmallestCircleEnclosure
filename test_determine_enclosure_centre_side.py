from unittest import TestCase
from SimpleMath import MyLine2D
from SimpleMath import Point2D
from SimpleMath import perpendicular_bisector
from SCE_Nimrod import determine_enclosure_centre_side
from SCE_Nimrod import form_angle_to_pair_map
from SCE_Nimrod import get_median_line
from SCE_Direct import find_smallest_circle_directly
from math import copysign
from math import pi
from math import radians
from test_reduced_circle import generate_random_points_list
from TimeMeasureDecorator import function_call_log_decorator
import readwrite_list

__author__ = 'Andrey'
#perrin


class TestDetermine_enclosure_centre_side(TestCase):

    def internal_test_the_list(self, lst, line=MyLine2D(coefs=[0.0, 1.0, 0.0])):
        circle, dumby = find_smallest_circle_directly(lst)
        side_sign = determine_enclosure_centre_side(lst, line)
        dist = line.distance_to_point(circle.centre)
        expected_sign = copysign(1, dist)
        self.assertEqual(expected_sign, side_sign)

    def internal_test_from_file(self, filename):
        line1 = MyLine2D(coefs=[1.0, 0.0, 0.0])
        line2 = MyLine2D(coefs=[1.0, 1.0, 0.0])
        line3 = MyLine2D(coefs=[0.8, -0.7, 2.0])
        ppp = readwrite_list.read_list_of_points(filename)
        self.internal_test_the_list(ppp)
        self.internal_test_the_list(ppp, line1)
        self.internal_test_the_list(ppp, line2)
        self.internal_test_the_list(ppp, line3)

    @function_call_log_decorator
    def test_small(self):
        ppp = [
            Point2D(-2.0, 3.0),
            Point2D(-1.0, -1.0),
            Point2D(-0.2, 3.5),
            Point2D(1.5, 0.6),
            Point2D(2.0, -0.1)
        ]
        self.internal_test_the_list(ppp)

    @function_call_log_decorator
    def test_40(self):
        self.internal_test_from_file("TestDetermineSide40.txt")

    @function_call_log_decorator
    def test_60(self):
        self.internal_test_from_file("TestDetermineSide60.txt")

    @function_call_log_decorator
    def test_secondary(self):
        print "test is here"
        self.assertTrue(True)

    @function_call_log_decorator
    def test_form_angle_to_pair_map(self):
        half_pi = pi * 0.5
        for i in range(100):
            p = generate_random_points_list(10, 20.0)
            angle_to_pair_map = form_angle_to_pair_map(p)
            for k in angle_to_pair_map.keys():
                self.assertTrue(abs(k) <= half_pi)

    @function_call_log_decorator
    def test_get_median_line_small_even(self):
        p = [Point2D(-2.0, 2.0),
             Point2D(-1.0, 1.0),
             Point2D(2.0, 0.0),
             Point2D(2.0, 2.0),
             Point2D(4.0, -1.0),
             Point2D(3.0, -2.0)]

        bisector = get_median_line(form_angle_to_pair_map(p))
        b = perpendicular_bisector(p[2], p[3])
        self.assertTrue(bisector.is_collinear(b))
        self.assertTrue(bisector.is_collinear(MyLine2D(coefs=[0.0, 1.0, 0.0])))

    @function_call_log_decorator
    def test_get_median_line_small_odd(self):
        p = [Point2D(-2.0, 2.0),
             Point2D(-1.0, 1.0),
             Point2D(2.0, 0.0),
             Point2D(2.0, 2.0),
             Point2D(4.0, -1.0),
             Point2D(3.0, -2.0),
             Point2D(-1.0, -3.0),
             Point2D(1.0, -2.0)]

        bisector = get_median_line(form_angle_to_pair_map(p))
        x_line = MyLine2D(coefs=[0.0, 1.0, 0.0])
        angle = bisector.angle(x_line)
        self.assertEqual(angle, radians(45.0 * 0.5))

