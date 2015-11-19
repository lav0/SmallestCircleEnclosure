import matplotlib.pyplot as plt
from SimpleMath import Point2D
from SCE_Direct import find_smallest_circle_directly
from SCE_ReduceCircle import find_smallest_circle_sqtime


list_of_points = list()


def circle_to_plt(circle, color='b'):
    return plt.Circle(
        (circle.centre.get_x(), circle.centre.get_y()),
        circle.radius,
        fill=False,
        color=color)


def button_press_callback(event):
    global list_of_points, circle1, circle2

    if event.button != 1:
        backup1, backup2 = circle1, circle2
        circle1, pivot_points1 = find_smallest_circle_directly(list_of_points)
        circle2, pivot_points2 = find_smallest_circle_sqtime(list_of_points)
        print str(len(list_of_points)) + " points"
        if circle1 is not None:
            circle1 = circle_to_plt(circle1)
            if backup1 is not None:
                backup1.remove()
            plt.gcf().gca().add_artist(circle1)
        if circle2 is not None:
            circle2 = circle_to_plt(circle2)
            if backup2 is not None:
                backup2.remove()
            plt.gcf().gca().add_artist(circle2)

    else:
        list_of_points.append(Point2D(event.xdata, event.ydata))
        drawable_point = plt.Line2D((event.xdata, event.xdata), (event.ydata, event.ydata), marker='o', color='r')
        plt.gcf().gca().add_artist(drawable_point)

    plt.show()


if __name__ == '__main__':

    line = plt.Line2D((.2, .5, .6), (.8, .5, .7), marker='o', color='r')

    circle1 = None
    circle2 = None

    fig = plt.gcf()
    fig.add_subplot(111, aspect='equal')

    fig.canvas.mpl_connect('button_press_event', button_press_callback)

    plt.show()

else:
    print __name__