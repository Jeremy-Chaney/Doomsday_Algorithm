from datetime import date, datetime
from math import floor
import os
from random import randrange
import sys
import subprocess

# setting this to zero will eliminate the intermediate
# check for the doomsday of the year. This would be more
# similar to how you'd actually use it IRL
CHECK_YEAR = 1

DOW_List = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday"
]

MONTH_LIST = [
   #(month#, num days, month name, doomsday)
    (1,     31, "January",      3),
    (2,     28, "February",     28),
    (3,     31, "March",        14),
    (4,     30, "April",        4),
    (5,     31, "May",          9),
    (6,     30, "June",         6),
    (7,     31, "July",         11),
    (8,     31, "August",       8),
    (9,     30, "September",    5),
    (10,    31, "October",      10),
    (11,    30, "November",     7),
    (12,    31, "December",     12)
]

base_year   = 1000
max_year    = 3000

help_text = """
Usage : this tool is a quizing program to help learn and
        use the doomsday algorithm on randomly generated
        days.

        By default the year range is 1000-3000 but can be changed
        by modifying the base_year/max_year variables.

        By default the CHECK_YEAR selecter is 1, this will force
        you to input the year's doomsday value before calculating
        the desired day. Change to 0 if you want to skip the
        intermediate calculation and solve all the way for the date
        in your head.
"""

# define our clear function
def clear():
    """
    General function to clear regardless of OS
    """
    if sys.platform == 'win32':
        _ = os.system('cls')
    else:
        _ = os.system('clear')

def get_day_month(year, random_day):
    """
    Pass in the year and the number of days since Jan 1 of that year
    And this function will return the month, day, and string version
    of the month.
    """
    month = 0
    day = 0
    month_str = ""
    running_count = 0

    for m_num, num_days, m_str, mon_dd in MONTH_LIST:
        if year % 4 == 0:
            if m_num == 2:
                m_len = 29
            else:
                m_len = num_days
        else:
            m_len = num_days

        if running_count + m_len < random_day:
            running_count = running_count + m_len
        else:
            day = random_day - running_count
            month = m_num
            month_str = m_str
            break

    return month, day, month_str

def get_day_of_week(year_dday, month, day, year):
    """
    pass in the year's doomsday, as well as the month, day, year
    and return the day of the week that day is on.
    """
    # figure out what the doomsday is for given month
    for m_num, num_days, m_str, mon_dd in MONTH_LIST:
        if m_num == month:
            if year % 4 == 0:
                if month == 1 or month == 2:
                    month_dday = mon_dd + 1
                    break
                else:
                    month_dday = mon_dd
                    break
            else:
                month_dday = mon_dd
                break

    # find difference in the given day from the month's doomsday
    offset = day - month_dday

    # increase offset by 7 until it's a positive number
    while(offset < 0):
        offset = offset + 7

    # add offset to the year's doomsday and normalize to be between 0 and 6
    day_of_week = (year_dday + offset) % 7

    return day_of_week

def main():
    clear()
    print("~Doomsday Calculation Quizzer~")

    if len(sys.argv) > 1:
        if (sys.argv[1] == "help") or (sys.argv[1] == "h"):
            print(help_text)
            exit()

    # generate a random year in the given range
    year = str(randrange(base_year, max_year))

    # generate a random day in the given year (consider leap years)
    if int(year) % 4 == 0:
        num_days = randrange(0, 366)
    else:
        num_days = randrange(0, 365)
    month, day, month_str = get_day_month(int(year), num_days)

    # chop off the last two characters to get the century
    century = int(year[:len(year) - 2])

    # *00 years follow cycle of having doomsdays of:
    # tuesday -> sunday -> friday -> wednesday
    if century % 4 == 0:
        cent_dday = 2
    elif century % 4 == 1:
        cent_dday = 0
    elif century % 4 == 2:
        cent_dday = 5
    elif century % 4 == 3:
        cent_dday = 3
    else:
        print("ERROR : couldn't find century for " + year)

    year_last2 = int(year[len(year) - 2:])
    year_last2_dday = year_last2 + floor(year_last2 / 4)

    year_dday = (cent_dday + year_last2_dday) % 7

    if CHECK_YEAR == 1:
        guess_val = input("What is the Doomsday for the year " + year + "? ")

        if int(guess_val) == year_dday:
            print("Correct :)")
        else:
            print("Incorrect :(")
            print("Year " + str(century) + "00 had doomsday " + str(cent_dday) + ".")
            print(str(century) + "00 - " + year + " had " + str(floor(year_last2 / 4)) + " leap years.")
            print(str(cent_dday) + " + " + str(year_last2) + " + " + str(floor(year_last2 / 4)) + " = " + str(cent_dday + year_last2_dday))
            print(str(cent_dday + year_last2_dday) + " % 7 = " + str(year_dday) + " -> " + DOW_List[year_dday])

        print("The Doomsday of " + year + " is " + DOW_List[year_dday])

    guess_val = input("What is the Doomsday for the day " + month_str + " " + str(day) + ", " + year + "? ")

    doomsday = get_day_of_week(year_dday, month, day, int(year))

    if int(guess_val) == doomsday:
        print("Correct :)")
    else:
        print("Incorrect :(")

    print(month_str + " " + str(day) + ", " + year + " is a " + DOW_List[doomsday])

if __name__ == "__main__":
    main()
