from SimpleMath import Vector2D


def write_list_of_points(thelist, filename):
    f = open(filename, "w+")
    for p in thelist:
        f.write(str(p.get_x()) + ", " + str(p.get_y()) + "\n")
    f.close()


def read_list_of_points(filename):
    f = open(filename, "r")
    if f.mode is "r":
        thelist = list()
        lines = f.readlines()
        for line in lines:
            split = [s.strip() for s in line.split(",")]
            thelist.append(Vector2D(float(split[0]), float(split[1])))
    f.close()
    return thelist
