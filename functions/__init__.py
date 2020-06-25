import datetime
import definitions

strptime = datetime.datetime.strptime
timedelta = datetime.timedelta
start_time = definitions.START_TIME

def func(x):
    return strptime(start_time, '%m/%d/%Y %H:%M:%S.%f') + timedelta(seconds=x)