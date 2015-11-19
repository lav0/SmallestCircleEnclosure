from math import sqrt

epsilon = 1e-6


class Point2D():
    def __init__(self, x, y):
        self.m_x, self.m_y = x, y

    def sum(self, other):
        return Point2D(self.m_x + other.m_x, self.m_y + other.m_y)

    def sub(self, other):
        return Point2D(self.m_x - other.m_x, self.m_y - other.m_y)

    def scal(self, other):
        return self.m_x * other.m_x + self.m_y * other.m_y

    def multiply(self, coef):
        return Point2D(self.m_x * coef, self.m_y * coef)

    def inverted(self):
        return Point2D(-self.m_x, -self.m_y)

    def squared_norm(self):
        return self.m_x ** 2 + self.m_y ** 2

    def norm(self):
        return sqrt(self.squared_norm())

    def get_x(self):
        return self.m_x

    def get_y(self):
        return self.m_y

    def __eq__(self, other):
        return self.sub(other).norm() < epsilon


class MyCircle():
    def __init__(self, p, r=1.0):
        self.centre, self.radius = p, r

    def is_point_on_edge(self, point):
        distance_to_centre = point.sub(self.centre).norm()
        return abs(distance_to_centre - self.radius) < epsilon

    def is_point_inside(self, point):
        distance_to_centre = point.sub(self.centre).norm()
        return distance_to_centre < self.radius + epsilon


def construct_circle_on_pair(p1, p2):
    centre = p1.sum(p2).multiply(0.5)
    radius = p1.sub(p2).norm() * 0.5
    return MyCircle(centre, radius)


def construct_circle_on_triple(p1, p2, p3):
    myline = MyLine2D(p1, p2)
    na1, nb1, dumb = myline.coefs()
    n1 = Point2D(na1, nb1)
    middle1 = myline.middle_point()
    myline = MyLine2D(p2, p3)
    na2, nb2, dumb = myline.coefs()
    n2 = Point2D(na2, nb2)
    middle2 = myline.middle_point()

    line1 = MyLine2D(middle1, middle1.sum(n1))
    line2 = MyLine2D(middle2, middle2.sum(n2))
    point = line1.intersection(line2)

    if point is None:
        # points are on the same line. take two points at ends
        vertices = sorted([p1, p2, p3], key=lambda v: v.get_x() + v.get_y())
        return construct_circle_on_pair(vertices[0], vertices[2])
    else:
        sub = point.sub(p1)
        radius = sqrt(sub.get_x() ** 2 + sub.get_y() ** 2)
        return MyCircle(point, radius)


class MyLine2D():
    def __init__(self, point1, point2):
        self.first = point1
        self.second = point2
        self.direc = point2.sub(point1)

    # coefficients (A,B,C) in form: Ax + By = C
    def coefs(self):
        yy = self.second.get_y() - self.first.get_y()
        xx = self.second.get_x() - self.first.get_x()
        return yy, -xx, yy * self.first.get_x() - xx * self.first.get_y()

    def orthogonal_vector(self):
        yy, xx, cc = self.coefs()
        return Point2D(yy, xx)

    def intersection(self, other):
        a1, b1, c1 = self.coefs()
        a2, b2, c2 = other.coefs()
        result = solve_simple_linear_system_cramer(a1, b1, c1, a2, b2, c2)
        if result is None: return None
        return Point2D(result[0], result[1])

    def middle_point(self):
        return self.first.sum(self.second).multiply(0.5)


def solve_simple_linear_system_cramer(a1, b1, c1, a2, b2, c2):
    #
    #  a1*x + b1*y = c1
    #  a2*x + b2*y = c2
    #
    det = a1 * b2 - a2 * b1;
    if abs(det) < epsilon:
        return None
    return [(c1 * b2 - c2 * b1) / det, (a1 * c2 - a2 * c1) / det]


def get_vertex_with_obtuse_angle(p1, p2, p3):
    #
    #  find obtuse angle of given triangle
    #
    squared_length1 = p1.sub(p2).squared_norm()
    squared_length2 = p2.sub(p3).squared_norm()
    squared_length3 = p3.sub(p1).squared_norm()

    tuple1 = (squared_length1, p3)
    tuple2 = (squared_length2, p1)
    tuple3 = (squared_length3, p2)

    thelist = sorted([tuple1, tuple2, tuple3], key=lambda tup: tup[0])

    if thelist[0][0] + thelist[1][0] >= thelist[2][0]:
        return None

    return thelist[2][1]