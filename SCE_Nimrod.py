import SimpleMath
from SimpleMath import Point2D
from SimpleMath import MyLine2D
from SimpleMath import perpendicular_bisector
from SCE_Direct import find_constrained_centre
from numpy import median as npmedian
from numpy import array
from math import copysign

__author__ = 'lav'


# critical value
def pair_bisector_and_line_intersection(point1, point2, line):
    bisector = perpendicular_bisector(point1, point2)
    return bisector.intersection(line)


def median_along_line(critical_points, line):
    v = list()
    for p in critical_points:
        v.append(line.direction_value_on_point(p))
    med_value = npmedian(array(v))
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


def along_line_cmp(line, point, val, greater):
    if greater:
        return line.direction_value_on_point(point) > val + SimpleMath.SM_ZERO
    else:
        return line.direction_value_on_point(point) < val - SimpleMath.SM_ZERO


def suspicious_points(critical_points, med, far, line):
    return [p for p in critical_points if along_line_cmp(line, p, med, far < med)]


def is_constrained_pointer_centre_found(median, farthest):
    return abs(farthest - median) < SimpleMath.SM_ZERO


def reject_redundant_points(lst, line):
    pairs = form_pairs(lst)
    critical_points = list()
    critpnt_to_pair_map = dict()
    rejected_points = list()
    for pair in pairs:
        intersection = pair_bisector_and_line_intersection(pair[0], pair[1], line)
        if intersection is None:
            if abs(line.distance_to_point(pair[0])) < abs(line.distance_to_point(pair[1])):
                rejected_points.append(pair[0])
            else:
                rejected_points.append(pair[1])
            continue
        critical_points.append(intersection)
        critpnt_to_pair_map[intersection] = pair

    #
    # for now we just handle a single point situation which is the most common
    # and natural one. for further consideration try to find all points whose
    # distance to the median point is ~(far-med) distance.
    #

    med = median_along_line(critical_points, line)
    far = max(lst, key=lambda p: med.sub(p).squared_norm())
    med_val = line.direction_value_on_point(med)
    far_val = line.direction_value_on_point(far)

    if is_constrained_pointer_centre_found(med_val, far_val):
        # the centre is found. need to handle
        pass

    suspicious_pnts = suspicious_points(critical_points, med_val, far_val, line)

    for x in suspicious_pnts:
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


def determine_enclosure_centre_side(lst, line):
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
                assert False

        for p in lst:
            if p in rejected:
                lst.remove(p)

    #print "Points count before direct search: ", len(lst)
    circle, pivots = find_constrained_centre(lst, line)
    print len(pivots)
    middle = pivots[0].sum(pivots[-1]).multiply(0.5)
    dist = line.distance_to_point(middle)

    return copysign(1, dist)




