import pytest
import sys

sys.path.append("../superpy")

from track_date import *
from datetime import date, timedelta


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
