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


def form_pairs(points):
    ln = len(points)
    half = ln // 2
    pairs = list()
    for i in range(half):
        t = (points[2*i], points[2*i+1])
        pairs.append(t)
    if ln % 2 == 1:
        t = (points[-1], points[0])
        pairs.append(t)
    return pairs


ppp = [Point2D(1.0, 0.0),
       Point2D(2.5, 1.0),
       Point2D(2.0, -1.5),
       Point2D(0.0, -1.9),
       Point2D(-0.5, 0.5),
       Point2D(-1.0, 0.0)]

qqq = form_pairs(ppp)
print [ (x[0].get_x(), x[0].get_y()) for x in qqq]
print [ (x[1].get_x(), x[1].get_y()) for x in qqq]
