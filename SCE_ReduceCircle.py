from __builtin__ import isinstance
from SimpleMath import Vector2D
from SimpleMath import MyCircle
from SimpleMath import Line2D
from SimpleMath import get_vertex_with_obtuse_angle
from SimpleMath import perpendicular_bisector
from TimeMeasureDecorator import time_measure_decorator


def reduced_circle_new(point1, point2, line):
    result = perpendicular_bisector(point1, point2).intersection(line)
    if result is None:
        raise ValueError("Cannot reduce circle")
    return MyCircle(result, result.sub(point1).norm())


def find_gravity_centre(a_list_of_points):
    inv_number_of_elements = 1.0 / len(a_list_of_points)
    return Vector2D(inv_number_of_elements * sum(p.get_x() for p in a_list_of_points),
                   inv_number_of_elements * sum(p.get_y() for p in a_list_of_points))


@time_measure_decorator
def find_smallest_circle_sqtime(a_list_of_points):
    gravity_centre = find_gravity_centre(a_list_of_points)
    smallest_circle = MyCircle(gravity_centre, .1)

    farther_point = max(a_list_of_points, key=lambda p: smallest_circle.centre.sub(p).norm())
    smallest_circle.radius = smallest_circle.centre.sub(farther_point).norm()

    anchor_radius = 0.0
    anchor_point = farther_point
    for p in a_list_of_points:
        if p is not farther_point:
            circle = reduced_circle_new(farther_point, p, Line2D(smallest_circle.centre, farther_point))
            if anchor_radius < circle.radius:
                anchor_radius = circle.radius
                anchor_point = p
                smallest_circle = circle

    # the pair of pivot points found:
    a = farther_point
    b = anchor_point

    in_progress = True
    while in_progress:
        in_progress = False

        two_points_based_centre = a.sum(b).multiply(0.5)
        two_points_based_radius = 0.5 * a.sub(b).norm()
        two_points_based_circle = MyCircle(two_points_based_centre, two_points_based_radius)

        if all(two_points_based_circle.is_point_inside(p) for p in a_list_of_points):
            smallest_circle = two_points_based_circle
            pivot_points = [a, b]
        else:
            final_radius = two_points_based_radius
            final_point = None
            final_centre = smallest_circle.centre
            for p in a_list_of_points:
                if p is not a and p is not b:
                    obtuse_point = get_vertex_with_obtuse_angle(a, b, p)
                    if obtuse_point is p:
                        continue

                    line_ab = Line2D(a, b)
                    mid = line_ab.middle_point()
                    line_along = Line2D(mid, mid.sum(line_ab.orthogonal_vector()))
                    circle = reduced_circle_new(a, p, line_along)
                    if final_radius < circle.radius < smallest_circle.radius:
                        final_radius = circle.radius
                        final_centre = circle.centre
                        final_point = p

#            assert isinstance(final_point, Point2D)
            obtuse_point = get_vertex_with_obtuse_angle(a, b, final_point)
            if obtuse_point is not None:
                assert final_point is not obtuse_point, 'final is obtuse!'
                in_progress = True
                if obtuse_point is a:
                    a = final_point
                else:
                    b = final_point
            else:
                smallest_circle.centre = final_centre
                smallest_circle.radius = final_radius
#                assert final_point is not a and not b
                if final_point is not None:
                    pivot_points = [a, b, final_point]
                else:
                    pivot_points = [a, b]

    assert isinstance(pivot_points, list)

    return smallest_circle, pivot_points
