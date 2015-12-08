import time


def time_measure_decorator(function):
    def wrapper(*arg, **kw):
        before = time.time()
        result = function(*arg, **kw)
        after = time.time()
        print str(after - before) + " seconds. Function:", function.__name__
        return result

    return wrapper


__author__ = 'Andrey'
