import unittest
from unittest import TestCase
from exp4_draw_clicks import Point2D
from exp4_draw_clicks import MyCircle
from exp4_draw_clicks import reduced_circle
from exp4_draw_clicks import get_vertex_with_obtuse_angle
from math import pi
from math import sin
from math import cos
import random

__author__ = 'lav'


class TestReduced_circle(unittest.TestCase):

    def get_random_point(self):
        return Point2D(random.uniform(-10.0, 10.0), random.uniform(-10.0, 10.0))

    def test_random(self):
        point_on = self.get_random_point()
        point_centre = self.get_random_point()
        norm = point_on.sub(point_centre).norm()
        circle = MyCircle(point_centre.get_x(), point_centre.get_y(), norm)

        self.assertTrue(circle.is_point_on_edge(point_on))

        point_along = self.get_random_point()
        point_aim = self.get_random_point()

        new_circle = reduced_circle(circle, point_on, point_along, point_aim);

        self.assertTrue(new_circle.is_point_on_edge(point_on))
        self.assertTrue(new_circle.is_point_on_edge(point_aim))

    def test_triangle_obtuse(self):
        point1 = Point2D(0, 0)
        point2 = Point2D(5, 0)
        point3 = Point2D(4, 4)

        self.assertEqual(None, get_vertex_with_obtuse_angle(point1, point2, point3));

        point4 = Point2D(4, 1)

        obtuse_point1 = get_vertex_with_obtuse_angle(point1, point2, point4)
        obtuse_point2 = get_vertex_with_obtuse_angle(point1, point4, point2)
        obtuse_point3 = get_vertex_with_obtuse_angle(point4, point2, point1)
        obtuse_point4 = get_vertex_with_obtuse_angle(point4, point1, point2)

        self.assertEqual(point4, obtuse_point1);
        self.assertEqual(point4, obtuse_point2);
        self.assertEqual(point4, obtuse_point3);
        self.assertEqual(point4, obtuse_point4);

    def test_reduced_circle(self):
        point_on = Point2D(1.0, .0)
        circle = MyCircle(.0, .0, 1.0)

        self.assertTrue(circle.is_point_on_edge(point_on))

        r = 0.75
        angle = 3 * pi / 4.0

        p0 = Point2D(r * cos(angle) + 0.25, r * sin(angle))
        p1 = Point2D(-0.5, .0);

        red_circle0 = reduced_circle(circle, point_on, point_on, p0)
        red_circle1 = reduced_circle(circle, point_on, point_on, p1)

        self.assertEqual(0.25, red_circle0.centre.get_x())
        self.assertEqual(0.0, red_circle0.centre.get_y())
        self.assertEqual(0.75, red_circle0.radius)
        self.assertEqual(0.25, red_circle1.centre.get_x())
        self.assertEqual(0.0, red_circle1.centre.get_y())
        self.assertEqual(0.75, red_circle1.radius)

        point_along = Point2D(0.5, 0.5);

        red_circle2 = reduced_circle(circle, point_on, point_along, p1);

        centre = red_circle2.centre;
        dist1 = centre.sub(point_on).norm();
        dist2 = centre.sub(p1).norm();

        self.assertEqual(dist1, red_circle2.radius)
        self.assertEqual(dist2, red_circle2.radius)

        self.test_triangle_obtuse()

        for i in range(500):
            self.test_random()



if __name__ == '__main__':
    unittest.main()
