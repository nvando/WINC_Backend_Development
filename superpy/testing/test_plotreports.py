# library imports
import sys
import os
import pytest
from datetime import date
import pandas as pd

# application imports
sys.path.append("../superpy")  # workaround to make tests work from within testing subfolder
from example_products import *
from plotreports import get_report
from ledger import Ledger


@pytest.fixture(autouse=True)
def run_after_tests():
    """Fixture to execute after each test is run:
    creates test csv files before running each function
    and cleanes them up afterwards"""

    # Setup:
    init_test_bought_csv()
    init_test_sold_csv()

    yield  # this is where the testing happens

    # Teardown
    if os.path.isfile(B_PATH):
        os.remove(B_PATH)
    if os.path.isfile(S_PATH):
        os.remove(S_PATH)


############################################################################
# Test functions for the 'get_report' function
# get_report takes as arguments:
# a report_month, as dateobject,
# a report function, (get_profit_day, get_revenue_day, get_product_sales)
# and a product name, only when report_method is set to 'get_product_sales')
# and returns a df


def test_get_report_of_revenue():

    ledger = Ledger(B_PATH, S_PATH)

    test_df = get_report(date(2021, 12, 1), ledger.get_revenue_day)
    test_df_aslist = test_df[1].tolist()

    assert isinstance((test_df), pd.DataFrame)
    # test for sold products on day 5(4.5), 6(2.5) and 7(1)
    assert len(test_df_aslist) == 31
    assert test_df_aslist == [
        0,0,0,0,4.5,2.5,1,0,
        0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0
        ]  # fmt: skip


def test_get_report_of_profit():

    ledger = Ledger(B_PATH, S_PATH)

    test_df = get_report(date(2021, 12, 1), ledger.get_profit_day)
    test_df_aslist = test_df[1].tolist()

    assert isinstance((test_df), pd.DataFrame)
    # test with bought products on day 4(2), 5(2.1), 6(6.3), 7(2.0) and 31 (3.2)
    # and for sold products on day 5(4.5), 6(2.5) and 7(1)
    assert len(test_df_aslist) == 31
    assert test_df_aslist == [
        0,0,0,-2,2.4,-3.8,-1,0,
        0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,-3.2
        ]  # fmt: skip


def test_get_report_of_product_sales():

    ledger = Ledger(B_PATH, S_PATH)

    test_df = get_report(date(2021, 12, 1), ledger.get_product_sales, "pear")
    test_df_aslist = test_df[1].tolist()

    assert isinstance((test_df), pd.DataFrame)
    # test with two pears sold on day 5
    assert len(test_df_aslist) == 31
    assert test_df_aslist == [
        0,0,0,0,2,0,0,0,
        0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0
        ]  # fmt: skip
