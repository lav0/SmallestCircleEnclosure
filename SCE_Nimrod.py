import SimpleMath
from SimpleMath import Vector2D
from SimpleMath import Line2D
from SimpleMath import perpendicular_bisector
from SCE_Direct import find_constrained_centre_directly
from test_reduced_circle import generate_random_points_list
from numpy import median as npmedian
from numpy import array
from math import copysign
from math import pi

__author__ = 'lav'


x_axis = Line2D(coefs=[0.0, 1.0, 0.0])
y_axis = Line2D(coefs=[1.0, 0.0, 0.0])


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
    perp_line = Line2D(None, None,
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


def reject_constrained_redundant_points(lst, line):
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


def determine_enclosure_centre_side(points, line):
    cpoints = list(points)
    while len(cpoints) > 3:
        rejected = reject_constrained_redundant_points(cpoints, line)
        if not rejected:
            chk1 = len(cpoints)
            last = cpoints[-1]
            cpoints.remove(last)
            cpoints.insert(0, last)
            chk2 = len(cpoints)
            assert chk1 == chk2
            rejected = reject_constrained_redundant_points(cpoints, line)
            if not rejected:
                assert False

        for p in cpoints:
            if p in rejected:
                cpoints.remove(p)

    print "Number of points before direct search: ", len(cpoints)
    circle, pivots = find_constrained_centre_directly(cpoints, line)
    middle = pivots[0].sum(pivots[-1]).multiply(0.5)
    dist = line.distance_to_point(middle)

    return copysign(1, dist)


def make_pair_to_bisector_map(points):
    pairs = form_pairs(points)
    result = dict()
    for pair in pairs:
        result[pair] = perpendicular_bisector(pair[0], pair[1])
    return result


def make_angle_to_bisector_map(points):
    bisectors = make_pair_to_bisector_map(points)
    result = dict()
    for b in bisectors.values():
        angle = x_axis.angle(b)
        if angle in result:
            assert False
        result[angle] = b
    return result


def get_median_bisector(angle_to_bisector_map):
    med_angle = npmedian(array(angle_to_bisector_map.keys()))
    if len(angle_to_bisector_map) % 2 == 1:
        bisector = angle_to_bisector_map[med_angle]
        return bisector
    else:
        angle_below = max([a for a in angle_to_bisector_map.keys() if a < med_angle])
        angle_above = min([a for a in angle_to_bisector_map.keys() if a > med_angle])
        line_below = angle_to_bisector_map[angle_below]
        line_above = angle_to_bisector_map[angle_above]

        def invert_if_x_less_zero(vector):
            return vector.inverted() if vector.get_x() < 0.0 else vector
        direction_below = invert_if_x_less_zero(line_below.direc.normalized())
        direction_above = invert_if_x_less_zero(line_above.direc.normalized())
        med_line_direction = direction_above.sum(direction_below)
        return Line2D(point1=Vector2D(0.0, 0.0), point2=med_line_direction)


def form_lines_pairs(points):
    angle_to_bisector = make_angle_to_bisector_map(points)
    med_bisector = get_median_bisector(angle_to_bisector)
    med_angle = x_axis.angle(med_bisector)
    angles_below = [a for a in angle_to_bisector.keys() if a < med_angle]
    angles_above = [a for a in angle_to_bisector.keys() if a > med_angle]
    assert len(angles_above) == len(angles_below)
    lines_pairs = list()
    for i in range(len(angles_below)):
        bisector_below = angle_to_bisector[angles_below[i]]
        bisector_above = angle_to_bisector[angles_above[i]]
        lines_pairs.append([bisector_below, bisector_above])
    if med_bisector in angle_to_bisector.values():
        lines_pairs.append([med_bisector, med_bisector])
    return lines_pairs


def form_pairs_intersections_values(lines_pairs, base_axis=y_axis):
    values = list()
    for pair in lines_pairs:
        intersection = pair[0].intersection(pair[1])
        if intersection is None:
            line0_value = base_axis.intersection(pair[0]).get_y()
            line1_value = base_axis.intersection(pair[1]).get_y()
            values.append(0.5 * (line0_value + line1_value))
        else:
            values.append(intersection.get_y())
    return values
