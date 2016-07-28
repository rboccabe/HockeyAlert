#!/usr/bin/python
# Author Ryan Boccabella
# Checks the current Pittsburgh Penguins schedule for a game and directs EST HH:MM time stamp on day of game to stdout
# If no game this day, directs 0 to stdout

from bs4 import BeautifulSoup
import urllib2
import datetime
import time
import sys

DATE_COLUMN=1
TIME_COLUMN=7

MONTH_TO_NUM = { 
                 'Jan' : 1,
                 'Feb' : 2,
                 'Mar' : 3,
                 'Apr' : 4,
                 'May' : 5,
                 'Jun' : 6,
                 'Jul' : 7,
                 'Aug' : 8,
                 'Sep' : 9,
                 'Oct' : 10,
                 'Nov' : 11,
                 'Dec' : 12
               }

def clean_dirty_date(dirty_tuple):
    (wkdy, month, date, year) = dirty_tuple
    return (MONTH_TO_NUM[month], int(date.rstrip(",")), int(year))

def is_date_match(date_tuple, year, month, day):
    if date_tuple == (month, day, year):
        return True
    else:
        return False

def format_time_of_game(time_string):
    (hour, half_2) = time_string.lstrip().rstrip().split(":")
    (minute, am_pm) = half_2.split(" ")
    if am_pm.find("P") != -1:
        hour = str(12 + int(hour))
    return hour+":"+minute
    
if len(sys.argv) == 4:
    try:
        date = datetime.date(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
    except ValueError as e:
        print 0
        sys.exit(0)
else:
    date=datetime.date.fromtimestamp(time.time())

cur_year=date.year
cur_month=date.month
cur_day=date.day

if cur_month in range(1,9):
    sched_start_year = cur_year - 1
else:
    sched_start_year = cur_year

season_arg=str(sched_start_year)+str(sched_start_year+1)

schedule_html = urllib2.urlopen('http://penguins.nhl.com/club/schedule.htm?season=' + season_arg + '&gametype=1').read()

game_dates = []
time_by_date = dict()

soup=BeautifulSoup(schedule_html, "lxml")
soup.prettify()
rows=soup.findAll('tr')
game_rows = 0
for row in rows:
    if 'class' in row.attrs:
        if 'rwOdd' in row['class'] or 'rwEven' in row['class']: 
            game_rows = game_rows + 1
            dirty_date_tuple = row.contents[DATE_COLUMN].string.split(" ")
            if (is_date_match(clean_dirty_date(dirty_date_tuple), cur_year, cur_month, cur_day)):
                print format_time_of_game(row.contents[TIME_COLUMN].string)
                sys.exit()
print 0
