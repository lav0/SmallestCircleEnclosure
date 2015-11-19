
from SimpleMath import construct_circle_on_pair
from SimpleMath import construct_circle_on_triple

import time


def time_measure_decorator(function):
    def wrapper(*arg, **kw):
        before = time.time();
        result = function(*arg, **kw);
        after = time.time();
        print str(after - before) + " seconds. Function:", function.__name__;
        return result

    return wrapper;


def check_and_replace(smallest_circle, circle, a_list_of_points):
    if smallest_circle is None or smallest_circle.radius > circle.radius:
        if all(circle.is_point_inside(p) for p in a_list_of_points):
            return circle, True

    return smallest_circle, False;


@time_measure_decorator
def find_smallest_circle_directly(a_list_of_points):
    smallest_circle = None;
    pivot_points = list()
    for p in a_list_of_points:
        for r in a_list_of_points:
            if p is not r:
                circle = construct_circle_on_pair(r, p);
                smallest_circle, reduced = check_and_replace(smallest_circle, circle, a_list_of_points);
                if reduced:
                    pivot_points = [p, r]
                for q in a_list_of_points:
                    if q is not p and q is not r:
                        circle = construct_circle_on_triple(p, r, q);
                        smallest_circle, reduced = check_and_replace(smallest_circle, circle, a_list_of_points);
                        if reduced:
                            pivot_points = [p, r, q]

    return smallest_circle, pivot_points;

