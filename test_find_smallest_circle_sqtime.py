from unittest import TestCase
from exp4_draw_clicks import find_smallest_circle_directly
from exp4_draw_clicks import find_smallest_circle_sqtime
from exp4_draw_clicks import find_gravity_centre
from exp4_draw_clicks import Point2D
from readwrite_list import write_list_of_points
from readwrite_list import read_list_of_points
import math
import random
__author__ = 'lav'


class TestFind_smallest_circle_sqtime(TestCase):

    def test_tricky(self):
        epsilon = 0.001
        delta   = math.sqrt(2 * epsilon - epsilon**2);

        p1 = Point2D(0.0, -1.0);
        p2 = Point2D(-1.0+epsilon, 0.9 * delta);
        p3 = Point2D(-math.cos(0.25*math.pi) + epsilon, math.sin(0.25*math.pi) - epsilon);

        thelist = [p1, p2, p3];

        gravity_centre = find_gravity_centre(thelist);
        zero_point = Point2D(.0, .0);

        while gravity_centre.sub(zero_point).norm() > 0.001:
            opposite_point = gravity_centre.inverted();
            thelist.append(opposite_point);
            thelist.append(opposite_point);
            thelist.append(opposite_point);
            gravity_centre = find_gravity_centre(thelist);

        circle1, pivot_points1 = find_smallest_circle_directly(thelist);
        circle2, pivot_point2 = find_smallest_circle_sqtime(thelist);

        self.assertEqual(round(circle1.centre.get_x(), 3), round(circle2.centre.get_x(), 3));
        self.assertEqual(round(circle1.centre.get_y(), 3), round(circle2.centre.get_y(), 3));
        self.assertEqual(round(circle1.radius, 3), round(circle2.radius, 3));


    def test_random(self, number_of_points, test_by_pivots = False):

        thelist = list();
        for i in range(number_of_points):
            thelist.append(Point2D(random.uniform(-10.0, 10.0), random.uniform(-10.0, 10.0)));

        write_list_of_points(thelist, "RandomPoints.txt");

        circle1, pivot_points1 = find_smallest_circle_directly(thelist);
        circle2, pivot_points2 = find_smallest_circle_sqtime(thelist);

        if test_by_pivots:
            p1_in_p2 = all(p in pivot_points1 for p in pivot_points2)
            p2_in_p1 = all(p in pivot_points2 for p in pivot_points1)

            self.assertTrue(p1_in_p2)
            self.assertTrue(p2_in_p1)
        else:
            self.assertEqual(round(circle1.centre.get_x(), 3), round(circle2.centre.get_x(), 3));
            self.assertEqual(round(circle1.centre.get_y(), 3), round(circle2.centre.get_y(), 3));
            self.assertEqual(round(circle1.radius, 3), round(circle2.radius, 3));

    def test_from_file(self, file_name, test_by_pivots = False):
        thelist = read_list_of_points(file_name);

        circle1, pivot_points1 = find_smallest_circle_directly(thelist);
        circle2, pivot_points2 = find_smallest_circle_sqtime(thelist);

        if test_by_pivots:
            p1_in_p2 = all(p in pivot_points1 for p in pivot_points2)
            p2_in_p1 = all(p in pivot_points2 for p in pivot_points1)

            self.assertTrue(p1_in_p2)
            self.assertTrue(p2_in_p1)
        else:
            self.assertEqual(round(circle1.centre.get_x(), 3), round(circle2.centre.get_x(), 3));
            self.assertEqual(round(circle1.centre.get_y(), 3), round(circle2.centre.get_y(), 3));
            self.assertEqual(round(circle1.radius, 3), round(circle2.radius, 3));


    def test_find_smallest_circle_sqtime(self):
        thelist = [Point2D(1.0, 0.0), Point2D(.5, .5), Point2D(-1.0, -0.25)];
        circle1, pivot_points = find_smallest_circle_directly(thelist);
        circle2, pivot_point2 = find_smallest_circle_sqtime(thelist);

        self.assertEqual(circle1.centre.get_x(), 0.0);
        self.assertEqual(circle1.centre.get_y(), -0.125);
        self.assertEqual(circle1.radius, 1.0077822185373186);
        self.assertEqual(circle2.centre.get_x(), 0.0);
        self.assertEqual(circle2.centre.get_y(), -0.125);
        self.assertEqual(circle2.radius, 1.0077822185373186);

        self.test_tricky(); print "Tricky test passed"
        self.test_from_file("TestCase0.txt"); print "File test passed"
        self.test_from_file("TestCase0.txt", test_by_pivots=True); print "File test passed"
        self.test_from_file("TestCase1.txt"); print "File test passed"
        self.test_from_file("TestCase1.txt", test_by_pivots=True); print "File test passed"
        self.test_from_file("TestCaseBig.txt"); print "File test passed"
        self.test_from_file("TestCase3.txt", test_by_pivots=True); print "File test passed"
        self.test_from_file("TestCase4.txt", test_by_pivots=True); print "File test passed"
        self.test_from_file("TestCase5.txt", test_by_pivots=True); print "File test passed"

        for i in range(1000):
            self.test_random(7, test_by_pivots=True); print "Random test %i passsed", i

        self.test_random(100)


