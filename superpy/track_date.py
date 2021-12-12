from pathlib import Path
from datetime import datetime, date, timedelta
import csv

# create a 'today file' if it does not exist
# or open it to retrieve the date that systems has stored as 'today'
if not Path("today.csv").is_file():
    TODAY = date.today()  # date-object does not include the time part
    with open("today.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(["todays_date", TODAY])
else:
    with open("today.csv", "r") as file:
        reader = csv.reader(file)
        TODAY = datetime.strptime(next(reader)[1], "%Y-%m-%d").date()


def valid_date(date_str):
    """validates whether the input date has format 'YYYY-MM-DD'
    or converts 'today' or 'yesterday' strings to a valid date.
    returns date-time object"""

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
            quit()
