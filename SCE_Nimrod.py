__author__ = 'lav'

from SimpleMath import Point2D
from SimpleMath import MyLine2D
from SimpleMath import perpendicular_bisector
from numpy import median
from numpy import array


# critical value
def pair_bisector_and_line_intersection(point1, point2, line):
    bisector = perpendicular_bisector(point1, point2)
    return bisector.intersection(line)


def median_along_line(critical_points, line):
    v = list()
    for p in critical_points:
        v.append(line.direction_value_on_point(p))
    med_value = median(array(v))
    codirect = line.direc
    perp_line = MyLine2D(None, None,
                         coefs=[codirect.get_x(), codirect.get_y(), med_value])
    result = perp_line.intersection(line)
    assert(result is not None)
    assert(line.is_point_on_line(result))
    return result


line = MyLine2D(Point2D(0, 0), Point2D(0, 1))

p1 = Point2D(0, 0.5)
p2 = Point2D(0, 1)
p3 = Point2D(0, 2)
p4 = Point2D(0, 4)

med = median_along_line([p1, p2, p3, p4], line)
print med.get_x(), med.get_y()