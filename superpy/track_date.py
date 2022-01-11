from pathlib import Path
from datetime import datetime, date, timedelta
import csv
import sys


# ------------------------------------------------------------------------------------
# Below functionality retrieves the date from today.csv
# in other to keep track of TODAY


if not Path("today.csv").is_file():  # create a 'today file' if it does not exist
    TODAY = date.today()
    with open("today.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(["todays_date", TODAY])

else:  # open today.csv to retrieve the date that has been stored as 'today'
    with open("today.csv", "r") as file:
        reader = csv.reader(file)
        TODAY = datetime.strptime(next(reader)[1], "%Y-%m-%d").date()


# -------------------------------------------------------------------------------------
# Below functions validate whether the CL arguments are in correct date format


def valid_date(date_str):
    """validates whether the input date has format 'YYYY-MM-DD'
    or converts 'today' or 'yesterday' strings to a valid date.
    returns date object"""

    if date_str == "today":
        date_obj = TODAY
        print("todays date = ", TODAY)
        return date_obj
    elif date_str == "yesterday":
        date_obj = TODAY - timedelta(days=1)
        print("yesterdays date is:", date_obj)
        return date_obj
    else:
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            print(
                f"{date_str} not a valid_date.",
                "Please enter a date in format 'YYYY-MM-DD'",
            )
            sys.exit()


def valid_month(date_str):
    """validates whether the input date has format 'YYYY-MM', returns date object"""

    try:
        return datetime.strptime(date_str, "%Y-%m").date()
    except ValueError:
        print(
            f"{date_str} not a valid month.",
            "Please enter a date in format 'YYYY-MM'",
        )
        sys.exit()


def valid_year(date_str):
    """validates whether the input date has format 'YYYY-MM', returns date object"""

    try:
        return datetime.strptime(date_str, "%Y").date()
    except ValueError:
        print(
            f"{date_str} not a valid year.",
            "Please enter a date in format 'YYYY'",
        )
        sys.exit()


# utility functions: seperated from functions in main.py which
# are called directly by the command line arguments
