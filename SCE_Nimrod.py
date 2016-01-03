import SimpleMath
from SimpleMath import Vector2D
from SimpleMath import Line2D
from SimpleMath import perpendicular_bisector
from SCE_Direct import find_constrained_centre_directly
from test_reduced_circle import generate_random_points_list
from numpy import median as npmedian
from numpy import array
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


def find_constrained_redundant_points(lst, line):
    pairs = form_pairs(lst)
    critical_points = list()
    critpnt_to_pair_map = dict()
    rejected_points = list()
    for pair in pairs:
        intersection = pair_bisector_and_line_intersection(pair[0], pair[1], line)
        if intersection is None:
            closest = min(pair, key=lambda p: abs(line.distance_to_point(p)))
            rejected_points.append(closest)
        else:
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
        rejected = find_constrained_redundant_points(cpoints, line)
        if not rejected:
            chk1 = len(cpoints)
            last = cpoints[-1]
            cpoints.remove(last)
            cpoints.insert(0, last)
            chk2 = len(cpoints)
            assert chk1 == chk2
            rejected = find_constrained_redundant_points(cpoints, line)
            if not rejected:
                assert False

        for p in cpoints:
            if p in rejected:
                cpoints.remove(p)

    print "Number of points before direct search: ", len(cpoints)
    circle, pivots = find_constrained_centre_directly(cpoints, line)
    middle = pivots[0].sum(pivots[-1]).multiply(0.5)
    return line.define_point_side(middle)


def make_bisector_to_pair_map(points):
    pairs = form_pairs(points)
    result = dict()
    for pair in pairs:
        bisector = perpendicular_bisector(pair[0], pair[1])
        result[bisector] = pair
    return result


def make_angle_to_bisector_map(bisector_to_pair_map):
    result = dict()
    for b in bisector_to_pair_map.keys():
        angle = x_axis.angle(b)
        if angle in result:
            assert False
        result[angle] = b
    return result


def get_median_bisector(angle_to_bisector_map):
    """
    :type angle_to_bisector_map: dict
    :rtype : Line2D
    """
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


def form_lines_pairs(angle_to_bisector_map, med_bisector):
    med_angle = x_axis.angle(med_bisector)
    angles_below = [a for a in angle_to_bisector_map.keys() if a < med_angle]
    angles_above = [a for a in angle_to_bisector_map.keys() if a > med_angle]
    assert len(angles_above) == len(angles_below)
    lines_pairs = list()
    for i in range(len(angles_below)):
        bisector_below = angle_to_bisector_map[angles_below[i]]
        bisector_above = angle_to_bisector_map[angles_above[i]]
        lines_pairs.append([bisector_below, bisector_above])
    if med_bisector in angle_to_bisector_map.values():
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


def get_y_separation_line(median_bisector, y_med):
    return Line2D(
        Vector2D(0.0, y_med),
        Vector2D(0.0, y_med).sum(median_bisector.direc)
    )


def define_cardinal_direction(y_separation_line, side, step_direction):
    point_south = y_separation_line.first.sum(step_direction)
    side_below = y_separation_line.define_point_side(point_south)

    if step_direction.is_collinear(y_axis.direc):
        ret_values = ["SOUTH", "NORTH"]
    else:
        ret_values = ["WEST", "EAST"]

    if side_below * side > 0:
        return ret_values[0]
    elif side_below * side < 0:
        return ret_values[1]

    # given arg 'side' seems to be zero
    print side, side_below
    assert False


def find_redundant_points(points):
    bisector_to_pair = make_bisector_to_pair_map(points)
    angle_to_bisector = make_angle_to_bisector_map(bisector_to_pair)
    median_bisector = get_median_bisector(angle_to_bisector)
    lines_pairs = form_lines_pairs(angle_to_bisector, median_bisector)
    ys_critical = form_pairs_intersections_values(lines_pairs)
    y_med = npmedian(array(ys_critical))
    y_separation_line = get_y_separation_line(median_bisector, y_med)
    aim_centre_y_side = determine_enclosure_centre_side(points, y_separation_line)
    critical_points = dict()
    for lines_pair in lines_pairs:
        intersection = lines_pair[0].intersection(lines_pair[1])
        if intersection is None:
            continue
        side = y_separation_line.define_point_side(intersection)
        if side * aim_centre_y_side <= 0:
            critical_points[intersection] = lines_pair
    xs_critical = [p.get_x() for p in critical_points]
    x_med = npmedian(array(xs_critical))
    x_separation_line = Line2D(point1=Vector2D(x_med, 0.0), point2=Vector2D(x_med, 1.0))
    aim_centre_x_side = determine_enclosure_centre_side(points, x_separation_line)
    crucial_lines_pairs = list()
    for p in critical_points.keys():
        side = x_separation_line.define_point_side(p)
        if side * aim_centre_x_side <= 0:
            crucial_lines_pairs.append(critical_points[p])

    south_north = define_cardinal_direction(y_separation_line, aim_centre_y_side, Vector2D(0.0, -1.0))
    east_west = define_cardinal_direction(x_separation_line, aim_centre_x_side, Vector2D(-1.0, 0.0))
    critical_lines = list()
    for lines_pair in crucial_lines_pairs:
        line0 = lines_pair[0]
        line1 = lines_pair[1]
        north = south_north == "NORTH"
        west = east_west == "WEST"
        if (north and west) or (not north and not west):
            angle0 = median_bisector.angle(line0)
            angle1 = median_bisector.angle(line1)
            assert angle0 * angle1 < 0
            if angle0 > 0:
                critical_lines.append(line0)
            else:
                critical_lines.append(line1)
        else:
            angle0 = median_bisector.angle(line0)
            angle1 = median_bisector.angle(line1)
            assert angle0 * angle1 < 0
            if angle0 < 0:
                critical_lines.append(line0)
            else:
                critical_lines.append(line1)

    rejected_points = list()
    for line in critical_lines:
        point1, point2 = bisector_to_pair[line]
        med_point = Vector2D(x_med, y_med)
        if line.are_points_on_same_side(point1, med_point):
            rejected_points.append(point1)
        elif line.are_points_on_same_side(point2, med_point):
            rejected_points.append(point2)
        else:
            assert True

    return rejected_points
