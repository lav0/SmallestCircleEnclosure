import unittest
import readwrite_list
import SimpleMath
from SCE_Nimrod import find_redundant_points
from SCE_Nimrod import make_bisector_to_pair_map
from SCE_Nimrod import make_angle_to_bisector_map
from SCE_Nimrod import get_median_bisector
from SCE_Nimrod import form_lines_pairs
from SCE_Nimrod import find_crucial_points
from SCE_Nimrod import scroll_points_list
from test_determine_enclosure_centre_side import get_default_points
from test_determine_enclosure_centre_side import get_extra_default_points
from test_reduced_circle import generate_random_points_list
from TimeMeasureDecorator import function_call_log_decorator

__author__ = 'Andrey'


def check_lists_equality(list1, list2):
    if len(list1) != len(list2):
        return False

    def check_one_way(l1, l2):
        for e in l1:
            if e not in l2:
                return False
        return True

    return check_one_way(list1, list2) and check_one_way(list2, list1)


def check_maps_equality(map1, map2):
    if len(map1) != len(map2):
        return False

    def check_one_way(m1, m2):
        for key in m1.keys():
            if key not in m2.keys():
                return False
            if m1[key] != m2[key]:
                return False
        return True

    return check_one_way(map1, map2) and check_one_way(map2, map1)


class MyTestCase(unittest.TestCase):
    @function_call_log_decorator
    def test_default(self):
        points = get_default_points()
        rejected = find_redundant_points(points)
        self.assertEqual(1, len(rejected))
        self.assertEqual(SimpleMath.Vector2D(-1.0, 1.0), rejected[0])
        points.remove(rejected[0])
        a = find_redundant_points(points)
        print [p.get_both() for p in a]

    def internal_test_loop(self, points):
        number_of_rejected = 1
        while number_of_rejected > 0:
            rejected = find_redundant_points(points)
            if not rejected:
                scroll_points_list(points)
                rejected = find_redundant_points(points)
            number_of_rejected = len(rejected)
            for r in rejected:
                if r not in points:
                    filename = "TestRejectedNotInGiven.txt"
                    readwrite_list.write_list_of_points(points, filename)
                points.remove(r)
        return len(points)

    def test_special(self):
        filename = "TestRejectedNotInGiven.txt"
        points = readwrite_list.read_list_of_points(filename)
        rejected = find_redundant_points(points)
        for r in rejected:
            if r not in points:
                print "NOT HERE ", r.get_both()

        print [p.get_both() for p in rejected]
        print [p.get_both() for p in points if -7.6 < p.get_x() < -7.4]

    @function_call_log_decorator
    def test_default1(self):
        points = get_extra_default_points()
        rejected = find_redundant_points(points)
        self.assertEqual(1, len(rejected))
        self.assertEqual(SimpleMath.Vector2D(-1.0, 1.0), rejected[0])

    @function_call_log_decorator
    def test_random(self):
        for i in range(10):
            points = generate_random_points_list(16, 20.0)
            readwrite_list.write_list_of_points(points, "Test1.txt")
            result_num = self.internal_test_loop(points)
            self.assertTrue(result_num < 16)

    @function_call_log_decorator
    def test_0(self):
        points = readwrite_list.read_list_of_points("Test0.txt")
        self.internal_test_loop(points)
        print [p.get_both() for p in points]

    @function_call_log_decorator
    def test_1(self):
        points = readwrite_list.read_list_of_points("Test1.txt")
        while len(points) > 4:
            rejected = find_redundant_points(points)
            if not rejected:
                scroll_points_list(points)
                rejected = find_redundant_points(points)
                if not rejected:
                    break
            for r in rejected:
                points.remove(r)
        print len(points)

    # @function_call_log_decorator
    # def test_something(self):
    #     points = get_default_points()
    #     sounth_counter = 0
    #     north_counter = 0
    #     west_counter = 0
    #     howmany = 100
    #     for i in range(howmany):
    #         south, west = find_redundant_points(points)
    #         points = generate_random_points_list(10 + 2 * i, 100.0)
    #         if south:
    #             sounth_counter += 1
    #         else:
    #             north_counter += 1
    #         if west:
    #             west_counter += 1
    #     print "SN: (", sounth_counter, north_counter, "), WE: (", west_counter, howmany - west_counter
    #     self.assertTrue(True)

    def internal_test_stability(self, pre_function, function):
        params = pre_function()
        exp_len = len(params)
        exp_result = function(params)
        for i in range(100):
            self.assertEqual(exp_len, len(params))
            result = function(params)
            if type(result) is dict:
                self.assertTrue(check_maps_equality(exp_result, result))
            elif type(result) is list:
                self.assertTrue(check_lists_equality(exp_result, result))

    @function_call_log_decorator
    def test_make_bisector_to_pair_map_stability(self):
        def pre_function():
            return generate_random_points_list(100, 100.0)
        self.internal_test_stability(pre_function, make_bisector_to_pair_map)

    @function_call_log_decorator
    def test_make_angle_to_bisector_map_stability(self):
        def pre_function():
            points = generate_random_points_list(100, 100.0)
            return make_bisector_to_pair_map(points)
        self.internal_test_stability(pre_function, make_angle_to_bisector_map)

    @function_call_log_decorator
    def test_form_lines_pairs_stability(self):
        points = generate_random_points_list(100, 100.0)
        bisector_to_pair = make_bisector_to_pair_map(points)
        angle_to_bisector = make_angle_to_bisector_map(bisector_to_pair)
        med_bisector = get_median_bisector(angle_to_bisector)
        exp_len = len(angle_to_bisector)
        exp_result = form_lines_pairs(angle_to_bisector, med_bisector)
        for i in range(100):
            self.assertEqual(exp_len, len(angle_to_bisector))
            result = form_lines_pairs(angle_to_bisector, med_bisector)
            self.assertTrue(check_lists_equality(exp_result, result))

    @function_call_log_decorator
    def test_find_crucial_points(self):
        points = readwrite_list.read_list_of_points("Test0.txt")
        line = SimpleMath.Line2D(coefs=[0.0, 1.0, 0.0])
        below = SimpleMath.Vector2D(0.0, -1.0)
        points_above = find_crucial_points(points, line, line.define_point_side(below))
        for p in points_above:
            self.assertTrue(p.get_y() >= 0.0)
        above = SimpleMath.Vector2D(0.0, 1.0)
        points_below = find_crucial_points(points, line, line.define_point_side(above))
        for p in points_below:
            self.assertTrue(p.get_y() <= 0.0)

if __name__ == '__main__':
    unittest.main()
