import matplotlib.pyplot as plt
import numpy as np
import time
from SimpleMath import epsilon
from SimpleMath import solve_simple_linear_system_cramer
from matplotlib.pyplot import eventplot


def time_measure_decorator(function):
    def wrapper(*arg, **kw):
        before = time.time();
        result = function(*arg, **kw);
        after = time.time();
        print str(after - before) + " seconds. Function:", function.__name__;
        return result

    return wrapper;


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
        return np.sqrt(self.squared_norm());

    def get_x(self):
        return self.m_x

    def get_y(self):
        return self.m_y

    def __eq__(self, other):
        return self.sub(other).norm() < epsilon;


class MyCircle():
    def __init__(self, x, y, r=1.0):
        self.centre, self.radius = Point2D(x, y), r;

    def is_point_on_edge(self, point):
        distance_to_centre = point.sub(self.centre).norm();
        return abs(distance_to_centre - self.radius) < epsilon;

    def is_point_inside(self, point):
        distance_to_centre = point.sub(self.centre).norm();
        return distance_to_centre < self.radius + epsilon;

    def to_plt(self, c='b'): return plt.Circle((self.centre.get_x(), self.centre.get_y()), self.radius, fill=False, color=c);


class MyLine2D():
    def __init__(self, point1, point2):
        self.first = point1
        self.second = point2
        self.direc = point2.sub(point1)

    # coefficients (A,B,C) in form: Ax + By = C
    def coefs(self):
        yy = self.second.get_y() - self.first.get_y();
        xx = self.second.get_x() - self.first.get_x();
        return yy, -xx, yy * self.first.get_x() - xx * self.first.get_y();

    def intersection(self, other):
        a1, b1, c1 = self.coefs();
        a2, b2, c2 = other.coefs();
        result = solve_simple_linear_system_cramer(a1, b1, c1, a2, b2, c2);
        if result is None: return None;
        return Point2D(result[0], result[1]);

    def middle_point(self):
        return self.first.sum(self.second).multiply(0.5)


def construct_circle_on_pair(p1, p2):
    centre = p1.sum(p2).multiply(0.5);
    radius = p1.sub(p2).norm() * 0.5;
    return MyCircle(centre.get_x(), centre.get_y(), radius);


def construct_circle_on_triple(p1, p2, p3):
    myline = MyLine2D(p1, p2);
    na1, nb1, dumb = myline.coefs();
    n1 = Point2D(na1, nb1);
    middle1 = myline.middle_point();
    myline = MyLine2D(p2, p3);
    na2, nb2, dumb = myline.coefs();
    n2 = Point2D(na2, nb2);
    middle2 = myline.middle_point();

    line1 = MyLine2D(middle1, middle1.sum(n1));
    line2 = MyLine2D(middle2, middle2.sum(n2));
    point = line1.intersection(line2);

    if point is None:
        triple = sorted([p1, p2, p3], key=lambda v: v.get_x() + v.get_y());
        return construct_circle_on_pair(triple[0], triple[2]);
    else:
        sub = point.sub(p1);
        radius = np.sqrt(sub.get_x() ** 2 + sub.get_y() ** 2);
        return MyCircle(point.get_x(), point.get_y(), radius);


def check_and_replace(smallest_circle, circle, list_of_points):
    if smallest_circle is not None:
        if smallest_circle.radius > circle.radius:
            if all(circle.is_point_inside(p) for p in list_of_points):
                smallest_circle = circle;
    else:
        if all(circle.is_point_inside(p) for p in list_of_points):
            smallest_circle = circle;
    return smallest_circle;


@time_measure_decorator
def find_smallest_circle_directly(list_of_points):
    smallest_circle = None;
    for p in list_of_points:
        for r in list_of_points:
            if p is not r:
                circle = construct_circle_on_pair(r, p);
                smallest_circle = check_and_replace(smallest_circle, circle, list_of_points);
                for q in list_of_points:
                    if q is not p and q is not r:
                        circle = construct_circle_on_triple(p, r, q);
                        smallest_circle = check_and_replace(smallest_circle, circle, list_of_points);

    return smallest_circle;


def reduced_circle(circle, point_on_circle, point_on_line_along, point_inside):
    #
    #   find a point (X,Y) on line lying on circle.centre and point_on_line_along such
    #   distances from (X,Y) to point_on_circle and to point_inside are same
    #
    xc, yc = circle.centre.get_x(), circle.centre.get_y();
    xa, ya = point_on_circle.get_x(), point_on_circle.get_y();
    xt, yt = point_on_line_along.get_x(), point_on_line_along.get_y();
    xp, yp = point_inside.get_x(), point_inside.get_y();

    #   first equation coefs
    a1 = yc - yt;
    b1 = xc - xt;
    c1 = a1 * xt - b1 * yt;

    #   second equation coefs
    a2 = 2*xa-2*xp;
    b2 = 2*ya-2*yp;
    c2 = xa**2-xp**2+ya**2-yp**2;

    result = solve_simple_linear_system_cramer(a1, -b1, c1, a2, b2, c2);
    if result is None: raise ValueError("Cannot reduce circle");
    new_point = Point2D(result[0],result[1]);
    return MyCircle(result[0], result[1], new_point.sub(point_on_circle).norm());

def find_gravity_centre(list_of_points):
    inv_number_of_elements = 1.0 / len(list_of_points);
    return Point2D(inv_number_of_elements * sum(p.get_x() for p in list_of_points),
                   inv_number_of_elements * sum(p.get_y() for p in list_of_points));

def is_triangle_obtuse(p1, p2, p3):
    squared_length1 = p1.sub(p2).squared_norm();
    squared_length2 = p2.sub(p3).squared_norm();
    squared_length3 = p3.sub(p1).squared_norm();

    thelist = sorted([squared_length1, squared_length2, squared_length3]);
    return thelist[0] + thelist[1] < thelist[2];


@time_measure_decorator
def find_smallest_circle_sqtime(list_of_points):
    gravity_centre = find_gravity_centre(list_of_points)
    smallest_circle = MyCircle(gravity_centre.get_x(),gravity_centre.get_y(), .1);

    farther_point = max(list_of_points, key=lambda p: smallest_circle.centre.sub(p).norm());
    smallest_circle.radius = smallest_circle.centre.sub(farther_point).norm();

    anchor_radius = 0.0;
    anchor_point = farther_point;
    for p in list_of_points:
        if p is not farther_point:
            circle = reduced_circle(smallest_circle, farther_point, farther_point, p);
            if anchor_radius < circle.radius:
                anchor_radius = circle.radius;
                anchor_point = p;

    # the pair of pivot points found:
    a = farther_point;
    b = anchor_point;

    pivot_centre = a.sum(b).multiply(0.5);
    pivot_radius = 0.5 * a.sub(b).norm();
    pivot_circle = MyCircle(pivot_centre.get_x(), pivot_centre.get_y(), pivot_radius);

    if all(pivot_circle.is_point_inside(p) for p in list_of_points):
        smallest_circle = pivot_circle;
    else:
        final_radius = 0;
        final_point = a;
        in_progress = True;
        while in_progress:
            pivot_centre = a.sum(b).multiply(0.5);
            for p in list_of_points:
                if p is not a and p is not b:
                    circle = reduced_circle(smallest_circle, a, pivot_centre, p);
                    if final_radius < circle.radius:
                        final_radius = circle.radius;
                        final_point = p;

            in_progress = is_triangle_obtuse(a, b, final_point);
            if in_progress:
                c = final_point;
                ab = b.sub(a);
                ac = c.sub(a);
                ba = a.sub(b);
                bc = c.sub(b);
                if ab.scal(ac) < 0:
                    list_of_points.remove(a);
                    a = final_point;
                elif ba.scal(bc) < 0:
                    list_of_points.remove(b);
                    b = final_point;
                else:
                    list_of_points.remove(final_point);
            else:
                smallest_circle = circle;



    return smallest_circle


list_of_points = list()


def button_press_callback(event):
    global list_of_points, circle1, circle2

    if event.button != 1:
        backup1, backup2 = circle1, circle2;
        circle1 = find_smallest_circle_directly(list_of_points);
        circle2 = find_smallest_circle_sqtime(list_of_points);
        print str(len(list_of_points)) + " points";
        if circle1 is not None:
            circle1 = circle1.to_plt('g');
            if backup1 is not None: backup1.remove();
            plt.gcf().gca().add_artist(circle1);
        if circle2 is not None:
            circle2 = circle2.to_plt();
            if backup2 is not None: backup2.remove();
            plt.gcf().gca().add_artist(circle2);

    else:
        list_of_points.append(Point2D(event.xdata, event.ydata))
        line = plt.Line2D((event.xdata, event.xdata), (event.ydata, event.ydata), marker='o', color='r')
        plt.gcf().gca().add_artist(line)

    plt.show()

if __name__ == '__main__':
    # sss = sorted( [3, 7, 6]);
    # print sss;

    line = plt.Line2D((.2, .5, .6), (.8, .5, .7), marker='o', color='r')

    circle1 = None;
    circle2 = None;

    fig = plt.gcf()
    fig.add_subplot(111, aspect='equal')

    fig.canvas.mpl_connect('button_press_event', button_press_callback)

    plt.show()

else:
    print __name__;