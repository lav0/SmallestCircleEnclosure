__author__ = 'lav'

import SimpleMath
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
    critpnt_to_pair_map = dict()
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
        critpnt_to_pair_map[intersection] = pair

    med = median_along_line(critical_points, line)
    far = max(lst, key=lambda p: med.sub(p).squared_norm())
    med_val = line.direction_value_on_point(med)
    far_val = line.direction_value_on_point(far)

    suspicious_points = list()
    if far_val > med_val:
        for p in critical_points:
            if line.direction_value_on_point(p) < med_val - SimpleMath.SM_ZERO:
                suspicious_points.append(p)
    elif far_val < med_val:
        for p in critical_points:
            if line.direction_value_on_point(p) > med_val + SimpleMath.SM_ZERO:
                suspicious_points.append(p)
    else:
        pass

    for x in suspicious_points:
        pair = critpnt_to_pair_map[x]
        bisector = perpendicular_bisector(pair[0], pair[1])
        med_sign = bisector.distance_to_point(med)
        if med_sign * bisector.distance_to_point(pair[0]) > 0:
            rejected_points.append(pair[0])
        elif med_sign * bisector.distance_to_point(pair[1]) > 0:
            rejected_points.append(pair[1])
        else:
            print med_sign, bisector.distance_to_point(pair[0]), bisector.distance_to_point(pair[1])
            assert False
    
    return rejected_points



