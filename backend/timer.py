from functools import wraps
from time import time
import datetime

def timed(f):
    @wraps(f) 
    def wrapper(*args, **kwds):
        start = time()
        f(*args, **kwds)
        end = time()
        time_taken = end - start
        time = datetime.datetime.now()
        with open("time_log.txt", "a") as f:
            f.write("(%s) time taken -> %d [at %s]" % (f.__name__, time_taken, time))
    return wrapper