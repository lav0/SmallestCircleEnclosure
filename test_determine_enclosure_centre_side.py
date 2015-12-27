from unittest import TestCase
from SimpleMath import Point2D
from SimpleMath import MyLine2D
from SCE_Nimrod import determine_enclosure_centre_side
from SCE_Direct import find_smallest_circle_directly
from math import copysign
from random import uniform

__author__ = 'Andrey'
#perrin
def generate_random_points_list(number_of_points, spread):
    thelist = list()
    for i in range(number_of_points):
        thelist.append(Point2D(uniform(-spread / 2, spread / 2), uniform(spread / 2, spread / 2)))
    return thelist


class TestDetermine_enclosure_centre_side(TestCase):

    def internal_test_the_list(self, lst, line=MyLine2D(coefs=[0.0, 1.0, 0.0])):
        side_sign = determine_enclosure_centre_side(lst, line)
        circle, dumby = find_smallest_circle_directly(lst)
        dist = line.distance_to_point(circle.centre)
        expected_sign = copysign(1, dist)
        self.assertEqual(expected_sign, side_sign)

    def test_main(self):
        line1 = MyLine2D(coefs=[1.0, 0.0, 0.0])
        line2 = MyLine2D(coefs=[1.0, 1.0, 0.0])
        line3 = MyLine2D(coefs=[0.8, -0.7, 2.0])
        for i in range(10):
            ppp = generate_random_points_list(10*(i+1), 20.0)
            self.internal_test_the_list(ppp)
            self.internal_test_the_list(ppp, line1)
            self.internal_test_the_list(ppp, line2)
            self.internal_test_the_list(ppp, line3)
