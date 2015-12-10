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
    assert (result is not None)
    assert (line.is_point_on_line(result))
    return result


def form_pairs(points):
    ln = len(points)
    half = ln // 2
    pairs = list()
    for i in range(half):
        t = (points[2 * i], points[2 * i + 1])
        pairs.append(t)
    if ln % 2 == 1:
        t = (points[-1], points[0])
        pairs.append(t)
    return pairs


def reject_redundant_points(lst, line):
    pairs = form_pairs(lst)
    critical_points = list()
    rejected_points = list()
    for pair in pairs:
        intersection = pair_bisector_and_line_intersection(pair[0], pair[1], line)
        if intersection is None:
            d0 = line.distance_to_point(pair[0])
            d1 = line.distance_to_point(pair[1])
            if abs(d0) < abs(d1):
                rejected_points.append(pair[0])
            else:
                rejected_points.append(pair[1])
            continue
        critical_points.append(intersection)

    med = median_along_line(critical_points, line)
    far = max(lst, key=lambda p: med.sub(p).squared_norm())
    med_val = line.direction_value_on_point(med)
    far_val = line.direction_value_on_point(far)

    suspicious_point = list()
    if far_val > med_val:
        for p in critical_points:
            if line.direction_value_on_point(p) < med_val:
                suspicious_point.append(p)
    elif far_val < med_val:
        for p in critical_points:
            if line.direction_value_on_point(p) > med_val:
                suspicious_point.append(p)
    else:
        pass

    
    return far


ppp = [Point2D(1.0, 0.0),
       Point2D(2.5, 1.0),
       Point2D(2.0, -1.5),
       Point2D(0.0, -1.9),
       Point2D(-0.5, 0.5),
       Point2D(-1.0, 0.0),
       Point2D(0.5, -1.0),
       Point2D(0.5, 1.5)]

line2 = MyLine2D(point1=Point2D(0.,1.), point2=Point2D(2.,0.))

med = reject_redundant_points(ppp, MyLine2D(coefs=[0.0, 1.0, 0.0]))
print med.get_x()
print med.get_y()

