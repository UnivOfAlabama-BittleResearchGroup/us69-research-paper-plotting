import datetime
import definitions
import time
from functools import wraps

strptime = datetime.datetime.strptime
timedelta = datetime.timedelta
# start_time = definitions.START_TIME

def func(x, start_time=None):
    return strptime(start_time, '%m/%d/%Y %H:%M:%S.%f') + timedelta(seconds=x)

def func_no_date(x, start_time=None):
    return strptime(start_time, '%H:%M:%S.%f') + timedelta(seconds=x)

def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time.time()
        result = f(*args, **kw)
        te = time.time()
        print('func:{0} took: {1} sec'.format(f.__name__, te - ts))
        return tuple([r for r in result] + [te - ts]) if isinstance(result, tuple) else (result, te - ts)
    return wrap
