from unittest import TestCase
from exp4_draw_clicks import find_smallest_circle_directly
from exp4_draw_clicks import find_smallest_circle_sqtime
from exp4_draw_clicks import find_gravity_centre
from exp4_draw_clicks import Point2D
import math
import random
__author__ = 'lav'


class TestFind_smallest_circle_sqtime(TestCase):

    def write_list_of_points(self, thelist, filename):
        f = open(filename, "w+")
        for p in thelist:
            f.write(str(p.get_x()) + ", " + str(p.get_y()) + "\n");
        f.close();

    def read_list_of_points(self, filename):
        f = open(filename, "r");
        if f.mode is "r":
            thelist = list();
            lines = f.readlines();
            for line in lines:
                split = [s.strip() for s in line.split(",")];
                thelist.append(Point2D(float(split[0]), float(split[1])))
        f.close();
        return thelist;

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

        circle1 = find_smallest_circle_directly(thelist);
        circle2 = find_smallest_circle_sqtime(thelist);

        self.assertEqual(round(circle1.centre.get_x(), 3), round(circle2.centre.get_x(), 3));
        self.assertEqual(round(circle1.centre.get_y(), 3), round(circle2.centre.get_y(), 3));
        self.assertEqual(round(circle1.radius, 3), round(circle2.radius, 3));


    def test_random(self):

        thelist = list();
        for i in range(10):
            thelist.append(Point2D(random.uniform(-10.0, 10.0), random.uniform(-10.0, 10.0)));

        self.write_list_of_points(thelist, "RandomPoints.txt");

        circle1 = find_smallest_circle_directly(thelist);
        circle2 = find_smallest_circle_sqtime(thelist);

        self.assertEqual(round(circle1.centre.get_x(), 3), round(circle2.centre.get_x(), 3));
        self.assertEqual(round(circle1.centre.get_y(), 3), round(circle2.centre.get_y(), 3));
        self.assertEqual(round(circle1.radius, 3), round(circle2.radius, 3));

    def test_from_file(self):
        thelist = self.read_list_of_points("TestCase0.txt");

        circle1 = find_smallest_circle_directly(thelist);
        circle2 = find_smallest_circle_sqtime(thelist);

        self.assertEqual(round(circle1.centre.get_x(), 3), round(circle2.centre.get_x(), 3));
        self.assertEqual(round(circle1.centre.get_y(), 3), round(circle2.centre.get_y(), 3));
        self.assertEqual(round(circle1.radius, 3), round(circle2.radius, 3));


    def test_find_smallest_circle_sqtime(self):
        thelist = [Point2D(1.0, 0.0), Point2D(.5, .5), Point2D(-1.0, -0.25)];
        circle1 = find_smallest_circle_directly(thelist);
        circle2 = find_smallest_circle_sqtime(thelist);

        self.assertEqual(circle1.centre.get_x(), 0.0);
        self.assertEqual(circle1.centre.get_y(), -0.125);
        self.assertEqual(circle1.radius, 1.0077822185373186);
        self.assertEqual(circle2.centre.get_x(), 0.0);
        self.assertEqual(circle2.centre.get_y(), -0.125);
        self.assertEqual(circle2.radius, 1.0077822185373186);

        self.test_tricky();
        self.test_from_file();
        self.test_random();
