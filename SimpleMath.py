from math import sqrt

epsilon = 1e-6;


class Point2D():
    def __init__(self, x, y):
        self.m_x, self.m_y = x, y

    def sum(self, other):
        return Point2D(self.m_x + other.m_x, self.m_y + other.m_y);

    def sub(self, other):
        return Point2D(self.m_x - other.m_x, self.m_y - other.m_y);

    def scal(self, other):
        return self.m_x * other.m_x + self.m_y * other.m_y;

    def multiply(self, coef):
        return Point2D(self.m_x * coef, self.m_y * coef);

    def inverted(self):
        return Point2D(-self.m_x, -self.m_y);

    def squared_norm(self):
        return self.m_x ** 2 + self.m_y ** 2

    def norm(self):
        return sqrt(self.squared_norm());

    def get_x(self):
        return self.m_x

    def get_y(self):
        return self.m_y

    def __eq__(self, other):
        return self.sub(other).norm() < epsilon;


def solve_simple_linear_system_cramer(a1, b1, c1, a2, b2, c2):
    #
    #  a1*x + b1*y = c1
    #  a2*x + b2*y = c2
    #
    det = a1 * b2 - a2 * b1;
    if abs(det) < epsilon:
        return None;
    return [(c1 * b2 - c2 * b1) / det, (a1 * c2 - a2 * c1) / det];
