# library imports
import sys
import pytest
from datetime import date, timedelta

# application imports
sys.path.append("../superpy")  # workaround to make tests work from within testing subfolder
from track_date import *


############################################################################
# tests for date manipulation functions


def test_set_date():
    set_date(date(2021, 12, 7))

    with open("today.csv", "r") as file:
        line = file.readline()

    assert line == "todays_date,2021-12-07\n"


def test_change_date():

    today = date(2021, 12, 7)
    assert change_date(today, 3) == date(2021, 12, 10)
    assert change_date(today, "2") == date(2021, 12, 9)
    assert change_date(today, -2) == date(2021, 12, 5)


############################################################################
# tests for date validation functions


def test_valid_date():
    global TODAY

    assert isinstance(valid_date("2021-12-2"), date)
    assert valid_date("today") == TODAY
    assert valid_date("yesterday") == TODAY - timedelta(days=1)
    assert valid_date("2021-12-2") == date(2021, 12, 2)


def test_valid_date_with_invalid_date():

    with pytest.raises(SystemExit) as wrapped_exception:
        valid_date("2021-12")
        assert wrapped_exception.type == SystemExit


def test_valid_month():

    assert isinstance(valid_month("2021-12"), date)
    assert valid_month("2021-12").month == 12
    assert valid_month("2021-12").year == 2021


def test_valid_month_with_invalid_date():

    with pytest.raises(SystemExit) as wrapped_exception:
        valid_month("2021-13")
        assert wrapped_exception.type == SystemExit


def test_valid_date_with_invalid_date():

    with pytest.raises(SystemExit) as wrapped_exception:
        valid_date("2021-12")
        assert wrapped_exception.type == SystemExit


def test_valid_year():

    assert isinstance(valid_year("2021"), date)
    assert valid_year("2021").year == 2021


def test_valid_month_with_invalid_date():

    with pytest.raises(SystemExit) as wrapped_exception:
        valid_year("202")
        assert wrapped_exception.type == SystemExit
