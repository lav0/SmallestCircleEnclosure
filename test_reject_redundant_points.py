from unittest import TestCase
from SimpleMath import Point2D
from SimpleMath import MyLine2D
from SCE_Direct import find_constrained_centre
from SCE_Nimrod import reject_redundant_points
from random import uniform

__author__ = 'lav'


class TestReject_redundant_points(TestCase):
    def easy_test_with_line(self, line):
        ppp = [Point2D(1.0, 0.0),
               Point2D(2.5, 1.0),
               Point2D(2.0, -1.5),
               Point2D(0.0, -1.9),
               Point2D(-0.5, 0.5),
               Point2D(-1.0, 0.0),
               Point2D(0.5, -1.0),
               Point2D(0.5, 1.5)]

        rejected = reject_redundant_points(ppp, line)

        self.assertEqual(len(rejected), 2)

        self.assertTrue(Point2D(0.5, -1.0) in rejected)
        self.assertTrue(Point2D(-0.5, 0.5) in rejected)

        for p in ppp:
            if p in rejected:
                ppp.remove(p)

        rejected = reject_redundant_points(ppp, line)

        self.assertEqual(len(rejected), 1)

        self.assertTrue(Point2D(0.5, 1.5) in rejected)

        for p in ppp:
            if p in rejected:
                ppp.remove(p)

        rejected = reject_redundant_points(ppp, line)

        self.assertEqual(len(rejected), 1)

        self.assertTrue(Point2D(1.0, 0.) in rejected)

    def internal_compare(self, lst, line):
        circle, points = find_constrained_centre(lst, line)

        while len(lst) > 3:
            rejected = reject_redundant_points(lst, line)
            if not rejected:
                chk1 = len(lst)
                last = lst[-1]
                lst.remove(last)
                lst.insert(0, last)
                chk2 = len(lst)
                assert chk1 == chk2
                rejected = reject_redundant_points(lst, line)
                if not rejected:
                    print "bad bad bad"

            for p in lst:
                if p in rejected:
                    lst.remove(p)

        for p in points:
            self.assertTrue(p in lst)

    def easy_test_with_line_based_on_direct_search(self, line):
        ppp = [Point2D(1.0, 0.0),
               Point2D(2.5, 1.0),
               Point2D(2.0, -1.5),
               Point2D(0.0, -1.9),
               Point2D(-0.5, 0.5),
               Point2D(-1.0, 0.0),
               Point2D(0.5, -1.0),
               Point2D(0.5, 1.5)]

        self.internal_compare(ppp, line)

    def internal_test_random(self, number_of_points, line):
        thelist = list()
        for i in range(number_of_points):
            thelist.append(Point2D(uniform(-10.0, 10.0), uniform(-10.0, 10.0)))
        self.internal_compare(thelist, line)

    def test_rejection(self):
        # easy test with hard-coded control points
        self.easy_test_with_line(MyLine2D(coefs=[0.0, 1.0, 0.0]))
        self.easy_test_with_line(MyLine2D(coefs=[0.0, 1.0, 0.131045525]))
        self.easy_test_with_line(MyLine2D(coefs=[0.0, 1.0, -0.15]))

        # tests with comparing to results found directly (by brute force)
        self.easy_test_with_line_based_on_direct_search(MyLine2D(coefs=[0.0, 1.0, 0.0]))
        self.easy_test_with_line_based_on_direct_search(MyLine2D(coefs=[1.0, 0.0, 0.0]))
        self.easy_test_with_line_based_on_direct_search(MyLine2D(coefs=[0.0, 1.0, 2.0]))
        self.easy_test_with_line_based_on_direct_search(MyLine2D(coefs=[1.0, 0.0, 2.0]))
        self.easy_test_with_line_based_on_direct_search(MyLine2D(coefs=[-1.0, 1.0, 0.0]))
        self.easy_test_with_line_based_on_direct_search(MyLine2D(coefs=[-1.0, 1.4, 3.0]))

        for i in range(10):
            self.internal_test_random(20, MyLine2D(coefs=[0.0, 1.0, 0.0]))
        for i in range(10):
            self.internal_test_random(100, MyLine2D(coefs=[0.0, 1.0, 0.0]))
        for i in range(5):
            print i, "wde range started"
            self.internal_test_random(400, MyLine2D(coefs=[0.0, 1.0, 0.0]))