
import os
import time
import datetime


fileLocation = r""
year = 2020
month = 1
day = 11
hour = 19
minute = 50
second = 0

date = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
modTime = time.mktime(date.timetuple())

os.utime('test.txt', (modTime, modTime))




def get_modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)

def get_creation_date(filename):
    t = os.path.getctime(filename)
    return datetime.datetime.fromtimestamp(t)


d = get_creation_date('test.txt')
print (d)

d = get_modification_date('test.txt')
print (d)




