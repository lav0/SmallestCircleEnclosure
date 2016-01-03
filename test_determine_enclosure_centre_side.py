from unittest import TestCase
from SimpleMath import Line2D
from SimpleMath import Vector2D
from SimpleMath import perpendicular_bisector
from SCE_Nimrod import determine_enclosure_centre_side
from SCE_Nimrod import make_angle_to_bisector_map
from SCE_Nimrod import get_median_bisector
from SCE_Nimrod import form_lines_pairs
from SCE_Nimrod import form_pairs_intersections_values
from SCE_Nimrod import form_pairs
from SCE_Nimrod import get_y_separation_line
from SCE_Nimrod import make_bisector_to_pair_map
from SCE_Direct import find_smallest_circle_directly
from math import copysign
from math import pi
from math import radians
from test_reduced_circle import generate_random_points_list
from TimeMeasureDecorator import function_call_log_decorator
import readwrite_list

__author__ = 'Andrey'


def get_default_points():
    return [Vector2D(2.0, 0.0),
            Vector2D(2.0, 2.0),
            Vector2D(4.0, -1.0),
            Vector2D(3.0, -2.0),
            Vector2D(-2.0, 2.0),
            Vector2D(-1.0, 1.0)]


class TestDetermine_enclosure_centre_side(TestCase):

    def internal_test_the_list(self, lst, line=Line2D(coefs=[0.0, 1.0, 0.0])):
        circle, dumby = find_smallest_circle_directly(lst)
        side_sign = determine_enclosure_centre_side(lst, line)
        dist = line.distance_to_point(circle.centre)
        expected_sign = copysign(1, dist)
        self.assertEqual(expected_sign, side_sign)

    def internal_test_from_file(self, filename):
        line1 = Line2D(coefs=[1.0, 0.0, 0.0])
        line2 = Line2D(coefs=[1.0, 1.0, 0.0])
        line3 = Line2D(coefs=[0.8, -0.7, 2.0])
        ppp = readwrite_list.read_list_of_points(filename)
        self.internal_test_the_list(ppp)
        self.internal_test_the_list(ppp, line1)
        self.internal_test_the_list(ppp, line2)
        self.internal_test_the_list(ppp, line3)

    @function_call_log_decorator
    def test_small(self):
        ppp = [
            Vector2D(-2.0, 3.0),
            Vector2D(-1.0, -1.0),
            Vector2D(-0.2, 3.5),
            Vector2D(1.5, 0.6),
            Vector2D(2.0, -0.1)
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
            angle_to_bisector_map = make_angle_to_bisector_map(make_bisector_to_pair_map(p))
            for k in angle_to_bisector_map.keys():
                self.assertTrue(abs(k) <= half_pi)

    @function_call_log_decorator
    def test_get_median_line_small_odd(self):
        p = get_default_points()
        bisector = get_median_bisector(make_angle_to_bisector_map(make_bisector_to_pair_map(p)))
        b = perpendicular_bisector(p[0], p[1])
        self.assertTrue(bisector.is_parallel(b))
        self.assertTrue(bisector.is_parallel(Line2D(coefs=[0.0, 1.0, 0.0])))

    @function_call_log_decorator
    def test_get_median_line_small_even(self):
        p = [Vector2D(-2.0, 2.0),
             Vector2D(-1.0, 1.0),
             Vector2D(2.0, 0.0),
             Vector2D(2.0, 2.0),
             Vector2D(4.0, -1.0),
             Vector2D(3.0, -2.0),
             Vector2D(-1.0, -3.0),
             Vector2D(1.0, -2.0)]

        bisector = get_median_bisector(make_angle_to_bisector_map(make_bisector_to_pair_map(p)))
        x_line = Line2D(coefs=[0.0, 1.0, 0.0])
        angle = bisector.angle(x_line)
        self.assertEqual(angle, radians(45.0 * 0.5))

    def internal_test_form_lines(self, p):
        angle_to_bisector = make_angle_to_bisector_map(make_bisector_to_pair_map(p))
        med_bisector = get_median_bisector(angle_to_bisector)
        lines_pairs = form_lines_pairs(angle_to_bisector, med_bisector)
        number_of_bisectors = len(form_pairs(p))
        if number_of_bisectors % 2 == 0:
            self.assertEqual(number_of_bisectors / 2, len(lines_pairs))
        else:
            self.assertEqual(number_of_bisectors / 2 + 1, len(lines_pairs))
        x_axis = Line2D(coefs=[0.0, 1.0, 0.0])
        median_bisector = get_median_bisector(make_angle_to_bisector_map(make_bisector_to_pair_map(p)))
        median_angle = x_axis.angle(median_bisector)
        for pair in lines_pairs:
            angle_below = x_axis.angle(pair[0])
            angle_above = x_axis.angle(pair[1])
            self.assertTrue(angle_below <= median_angle)
            self.assertTrue(angle_above >= median_angle)

    @function_call_log_decorator
    def test_form_lines_pairs(self):
        for i in range(10, 30):
            self.internal_test_form_lines(generate_random_points_list(i, 20.0))
            self.internal_test_form_lines(generate_random_points_list(i, 30.0))

    def internal_test_form_pairs_intersections_values(self, p, expected):
        angle_to_bisector = make_angle_to_bisector_map(make_bisector_to_pair_map(p))
        med_bisector = get_median_bisector(angle_to_bisector)
        lines_pairs = form_lines_pairs(angle_to_bisector, med_bisector)
        ys = form_pairs_intersections_values(lines_pairs)
        for e in expected:
            self.assertTrue(e in ys)

    def check_maps_equality(self, map1, map2):
        if len(map1) != len(map2):
            return False

        def check_one(m1, m2):
            for key in m1.keys():
                if key not in m2.keys():
                    return False
                if m1[key] != m2[key]:
                    return False
        return check_one(map1, map2) and check_one(map2, map1)

    def internal_test_stability(self, function, args):
        exp_len = len(args)
        exp_res = function(args)
        for i in range(1):
            self.assertEqual(exp_len, len(args))
            check_res = function(args)
            if not self.check_maps_equality(exp_res, check_res):
                print [p.direc.get_both() for p in exp_res]
                print [p.direc.get_both() for p in check_res]
                self.assertTrue(False)
        return exp_res

    def internal_test_form_pairs_intersections_values_stability(self, points):
        bisector_to_pair = self.internal_test_stability(make_bisector_to_pair_map, points)
        # angle_to_bisector = self.internal_test_stability(make_angle_to_bisector_map, bisector_to_pair)
        # med_bisector = get_median_bisector(angle_to_bisector)
        # lines_pairs = form_lines_pairs(angle_to_bisector, med_bisector)
        # ys = form_pairs_intersections_values(lines_pairs)

    @function_call_log_decorator
    def test_form_pairs_intersections_values_simple(self):
        p = get_default_points()
        exp = [1.0, 2.5]
        self.internal_test_form_pairs_intersections_values(p, exp)
        #self.internal_test_form_pairs_intersections_values_stability(p)

    @function_call_log_decorator
    def test_form_pairs_intersections_values_from_file(self):
        p = readwrite_list.read_list_of_points("TestDetermineSide20.txt")
        #self.internal_test_form_pairs_intersections_values_stability(p)
        exp = [1.7433726006528731,
               -0.15965496338328003,
               2.1813704343625773,
               3.6302737863622667,
               1.6106757565318828]
        self.internal_test_form_pairs_intersections_values(p, exp)

    def test_get_y_separation_line(self):
        bisector = Line2D(point1=Vector2D(0.0, 0.0), point2=Vector2D(2.0, 1.0))
        separation_line = get_y_separation_line(bisector, 3)
        y_axis_intersection = separation_line.intersection(Line2D(coefs=[1.0, 0.0, 0.0]))
        self.assertTrue(separation_line.is_parallel(bisector))
        self.assertEqual(y_axis_intersection.get_x(), 0.0)
        self.assertEqual(y_axis_intersection.get_y(), 3.0)
