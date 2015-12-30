import unittest
from unittest import TestCase
from SimpleMath import Vector2D
from SimpleMath import MyCircle
from SCE_ReduceCircle import reduced_circle_new
from SimpleMath import Line2D
from SimpleMath import get_vertex_with_obtuse_angle
from math import pi
from math import sin
from math import cos
from random import uniform

__author__ = 'lav'


def generate_random_point(spread):
    return Vector2D(uniform(-spread / 2, spread / 2), uniform(-spread / 2, spread / 2))


def generate_random_points_list(number_of_points, spread):
    thelist = list()
    for i in range(number_of_points):
        thelist.append(generate_random_point(spread))
    return thelist


class TestReduced_circle(unittest.TestCase):

    def get_random_point(self):
        return generate_random_point(20.0)

    def test_random(self):
        point_on = self.get_random_point()
        point_centre = self.get_random_point()
        norm = point_on.sub(point_centre).norm()
        circle = MyCircle(point_centre, norm)

        self.assertTrue(circle.is_point_on_edge(point_on))

        point_along = self.get_random_point()
        point_aim = self.get_random_point()

        new_circle_new = reduced_circle_new(point_on, point_aim, Line2D(circle.centre, point_along))

        self.assertTrue(new_circle_new.is_point_on_edge(point_on))
        self.assertTrue(new_circle_new.is_point_on_edge(point_aim))

    def test_triangle_obtuse(self):
        point1 = Vector2D(0, 0)
        point2 = Vector2D(5, 0)
        point3 = Vector2D(4, 4)

        self.assertEqual(None, get_vertex_with_obtuse_angle(point1, point2, point3));

        point4 = Vector2D(4, 1)

        obtuse_point1 = get_vertex_with_obtuse_angle(point1, point2, point4)
        obtuse_point2 = get_vertex_with_obtuse_angle(point1, point4, point2)
        obtuse_point3 = get_vertex_with_obtuse_angle(point4, point2, point1)
        obtuse_point4 = get_vertex_with_obtuse_angle(point4, point1, point2)

        self.assertEqual(point4, obtuse_point1);
        self.assertEqual(point4, obtuse_point2);
        self.assertEqual(point4, obtuse_point3);
        self.assertEqual(point4, obtuse_point4);

    def test_reduced_circle(self):
        point_on = Vector2D(1.0, .0)
        circle = MyCircle(Vector2D(.0, .0), 1.0)

        self.assertTrue(circle.is_point_on_edge(point_on))

        r = 0.75
        angle = 3 * pi / 4.0

        p0 = Vector2D(r * cos(angle) + 0.25, r * sin(angle))
        p1 = Vector2D(-0.5, .0);

        line = Line2D(circle.centre, point_on)
        red_circle_new0 = reduced_circle_new(point_on, p0, line)
        red_circle_new1 = reduced_circle_new(point_on, p1, line)

        self.assertEqual(0.25, red_circle_new0.centre.get_x())
        self.assertEqual(0.0, red_circle_new0.centre.get_y())
        self.assertEqual(0.75, red_circle_new0.radius)
        self.assertEqual(0.25, red_circle_new1.centre.get_x())
        self.assertEqual(0.0, red_circle_new1.centre.get_y())
        self.assertEqual(0.75, red_circle_new1.radius)

        self.test_triangle_obtuse()

        for i in range(500):
            self.test_random()


if __name__ == '__main__':
    unittest.main()

