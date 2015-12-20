from unittest import TestCase
from SimpleMath import Point2D
from SimpleMath import MyLine2D
from SCE_Nimrod import determine_enclosure_centre_side
from SCE_Direct import find_smallest_circle_directly
from math import copysign

__author__ = 'Andrey'


class TestDetermine_enclosure_centre_side(TestCase):
    def test_main(self):
        ppp = [Point2D(1.0, 0.0),
               Point2D(2.5, 1.0),
               Point2D(2.0, -1.5),
               Point2D(0.0, -1.9),
               Point2D(0.25, 1.9),
               Point2D(-0.5, 0.5),
               Point2D(-1.0, 0.0),
               Point2D(0.5, -1.0),
               Point2D(0.5, 1.5)]

        line = MyLine2D(coefs=[0.0, 1.0, 0.0])

        side_sign = determine_enclosure_centre_side(ppp, line)

        circle, dumby = find_smallest_circle_directly(ppp)

        dist = line.distance_to_point(circle.centre)
        expected_sign = copysign(1, dist)

        self.assertEqual(expected_sign, side_sign)
