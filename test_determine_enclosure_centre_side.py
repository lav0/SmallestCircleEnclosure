from unittest import TestCase
from SimpleMath import MyLine2D
from SimpleMath import Point2D
from SCE_Nimrod import determine_enclosure_centre_side
from SCE_Direct import find_smallest_circle_directly
from math import copysign
from test_reduced_circle import generate_random_points_list
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

    def test_small(self):
        ppp = [
            Point2D(-2.0, 3.0),
            Point2D(-1.0, -1.0),
            Point2D(-0.2, 3.5),
            Point2D(1.5, 0.6),
            Point2D(2.0, -0.1)
        ]
        self.internal_test_the_list(ppp)

    def test_40(self):
        self.internal_test_from_file("TestDetermineSide40.txt")

    def test_60(self):
        self.internal_test_from_file("TestDetermineSide60.txt")

    def test_secondary(self):
        print "test is here"
        self.assertTrue(True)

