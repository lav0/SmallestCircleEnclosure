
from SimpleMath import construct_circle_on_pair
from SimpleMath import construct_circle_on_triple
from SimpleMath import point_to_line_projection
from SimpleMath import perpendicular_bisector
from SimpleMath import construct_circle_with_centre_and_point
from TimeMeasureDecorator import time_measure_decorator


def check_and_replace(smallest_circle, circle, a_list_of_points):
    if smallest_circle is None or smallest_circle.radius > circle.radius:
        if all(circle.is_point_inside(p) for p in a_list_of_points):
            return circle, True

    return smallest_circle, False;


def check_smaller_circle(cur_small,
                         lst,
                         pivot_points,
                         suspected_pivot,
                         circle_builder,
                         args):
    circle = circle_builder(*args)
    cur_small, reduced = check_and_replace(cur_small, circle, lst)
    if reduced:
        pivot_points = suspected_pivot
    return cur_small, pivot_points


@time_measure_decorator
def find_smallest_circle_directly(a_list_of_points):
    smallest_circle = None;
    pivot_points = list()
    for p in a_list_of_points:
        for r in a_list_of_points:
            if p is not r:
                smallest_circle, pivot_points = check_smaller_circle(smallest_circle,
                                                                     a_list_of_points,
                                                                     pivot_points,
                                                                     [p, r],
                                                                     construct_circle_on_pair,
                                                                     args=[r, p])
                for q in a_list_of_points:
                    if q is not p and q is not r:
                        circle = construct_circle_on_triple(p, r, q);
                        smallest_circle, reduced = check_and_replace(smallest_circle, circle, a_list_of_points);
                        if reduced:
                            pivot_points = [p, r, q]
                        smallest_circle, pivot_points = check_smaller_circle(smallest_circle,
                                                                             a_list_of_points,
                                                                             pivot_points,
                                                                             [p, r, q],
                                                                             construct_circle_on_triple,
                                                                             args=[p, r, q])

    return smallest_circle, pivot_points


def find_constrained_centre(lst, line):
        smallest_circle = None
        pivot_points = list()
        for p in lst:
            projection = point_to_line_projection(p, line)
            assert line.is_point_on_line(projection)
            smallest_circle, pivot_points = check_smaller_circle(smallest_circle,
                                                                 lst, pivot_points, [p],
                                                                 construct_circle_with_centre_and_point,
                                                                 args=[projection, p])
            for q in lst:
                if p is not q:
                    bisector = perpendicular_bisector(p, q)
                    intersection = bisector.intersection(line)
                    if intersection is not None:
                        smallest_circle, pivot_points = check_smaller_circle(smallest_circle,
                                                                             lst, pivot_points, [p, q],
                                                                             construct_circle_with_centre_and_point,
                                                                             args=[intersection, p])

        return smallest_circle, pivot_points


