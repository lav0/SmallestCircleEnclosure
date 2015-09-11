import unittest
from unittest import TestCase
from exp4_draw_clicks import Point2D
from exp4_draw_clicks import MyCircle
from exp4_draw_clicks import reduced_circle
from math import pi
from math import sin
from math import cos

__author__ = 'lav'


class TestReduced_circle(unittest.TestCase):
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

if __name__ == '__main__':
    unittest.main()
