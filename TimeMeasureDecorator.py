import time


def time_measure_decorator(function):
    def wrapper(*arg, **kw):
        before = time.time()
        result = function(*arg, **kw)
        after = time.time()
        print str(after - before) + " seconds. Function:", function.__name__
        return result

    return wrapper


def function_call_log_decorator(function):
    def wrapper(*arg, **kw):
        print "\nFunction ", function.__name__, " started"
        result = function(*arg, **kw)
        print "Finished ", function.__name__
        return result

    return wrapper


__author__ = 'Andrey'
