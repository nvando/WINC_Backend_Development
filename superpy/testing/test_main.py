import sys

sys.path.append("../superpy")
from main import *

from datetime import date
import os
import pytest
from example_products import *
from ledger import Ledger
import pandas as pd


# Fixture to execute after each test is run:
# If test csv files are created in a test function
# this makes sure they are cleaned up even if the test failes
@pytest.fixture(autouse=True)
def run_after_tests(tmpdir):

    yield  # this is where the testing happens

    # Teardown
    if os.path.isfile(B_PATH):
        os.remove(B_PATH)
    if os.path.isfile(S_PATH):
        os.remove(S_PATH)


############################################################################
# tests for date manipulation functions


def test_set_date():
    set_date(date(2021, 12, 7))

    with open("today.csv", "r") as file:
        line = file.readline()

    assert line == "todays_date,2021-12-07\n"


def test_advance_time():

    today = date(2021, 12, 7)
    assert advance_time(today, 3) == date(2021, 12, 10)
    assert advance_time(today, "2") == date(2021, 12, 9)
    assert advance_time(today, -2) == date(2021, 12, 5)


############################################################################
# testing the create_csv function


def test_create_csv():

    create_csv("test", ["heading1", "heading2"])
    assert os.path.isfile("test")

    with open("test", "r") as file:
        line = file.readline()

        assert line == "heading1,heading2\n"

    os.remove("test")


############################################################################
# tests for the buy product function


def test_buy_product_new_file_single_product():

    # test with no existing file and product quantity = 1
    buy_product("apple", date(2021, 10, 1), 2.3, date(2021, 12, 12), 1, B_PATH)
    with open(B_PATH, "r") as file:
        lines = file.readlines()
        assert lines[0] == "id,product,buy_date,buy_price,expiration\n"
        assert lines[1] == "1,apple,2021-10-01,2.3,2021-12-12\n"


def test_buy_product_new_file_multiple_products():
    # test with no exiting file and product quantity = 3
    buy_product("apple", date(2021, 10, 1), 2.3, date(2021, 12, 12), 3, B_PATH)
    with open(B_PATH, "r") as file:
        lines = file.readlines()
        assert lines[0] == "id,product,buy_date,buy_price,expiration\n"
        assert lines[1] == "1,apple,2021-10-01,2.3,2021-12-12\n"
        assert lines[2] == "2,apple,2021-10-01,2.3,2021-12-12\n"
        assert lines[3] == "3,apple,2021-10-01,2.3,2021-12-12\n"


def test_buy_product_existing_file_single_product():

    init_test_bought_csv()

    buy_product("apple", date(2021, 10, 1), 2.3, date(2021, 12, 12), 1, B_PATH)

    # test whether product is added as row 10, after existing product on row 9
    with open(B_PATH, "r") as file:
        lines = file.readlines()
        assert lines[9] == "9,banana,2021-12-31,3.2,2042-01-01\n"
        assert lines[10] == "10,apple,2021-10-01,2.3,2021-12-12\n"


def test_buy_product_existing_file_multiple_products():

    # initialize 'dummy' csv-file to test with 10 rows
    init_test_bought_csv()

    # test if multiple rows are added after existing row 9
    # if quantity > 1
    buy_product("apple", date(2021, 10, 1), 2.3, date(2021, 12, 12), 3, B_PATH)

    with open(B_PATH, "r") as file:
        lines = file.readlines()
        assert lines[9] == "9,banana,2021-12-31,3.2,2042-01-01\n"
        assert lines[10] == "10,apple,2021-10-01,2.3,2021-12-12\n"
        assert lines[11] == "11,apple,2021-10-01,2.3,2021-12-12\n"
        assert lines[12] == "12,apple,2021-10-01,2.3,2021-12-12\n"


############################################################################
# tests for the sell product function


def test_sell_product_new_file_single_product():

    # test with no existing sold file and product quantity = 1
    init_test_bought_csv()

    sell_product("apple", date(2021, 12, 8), 3.5, 1, B_PATH, S_PATH)

    # test whether product gets added to inventory
    # and are not expired
    with open(S_PATH, "r") as file:
        lines = file.readlines()
        # check header
        assert lines[0] == "id,bought_id,sell_date,sell_price\n"
        # skip bought_id 1, expired apple, add 2nd apple with bought_id 4
        assert lines[1] == "1,4,2021-12-08,3.5\n"


def test_sell_product_new_file_multiple_products():
    # test with no existing sold file and product quantity = 3

    init_test_bought_csv()

    sell_product("apple", date(2021, 12, 8), 3.5, 3, B_PATH, S_PATH)

    # test whether product gets added to inventory
    # and are not expired
    with open(S_PATH, "r") as file:
        lines = file.readlines()
        # check headers
        # skip bought_id 1, expired apple, add 2nd apple with bought_id 4
        assert lines[0] == "id,bought_id,sell_date,sell_price\n"
        assert lines[1] == "1,4,2021-12-08,3.5\n"
        assert lines[2] == "2,5,2021-12-08,3.5\n"
        assert lines[3] == "3,6,2021-12-08,3.5\n"


def test_sell_product_existing_file_single_product():

    # test with existing sold file and product quantity = 1
    init_test_bought_csv()
    init_test_sold_csv()

    sell_product("apple", date(2021, 12, 8), 3.5, 1, B_PATH, S_PATH)

    # test whether product gets added to inventory
    # and is not expired
    # and has not ben sold already
    with open(S_PATH, "r") as file:
        lines = file.readlines()
        # check headers
        # skip bought_id 1 (expired apple) and bought_id 4 (apple already sold)
        # add apple with bought_id 5
        assert lines[0] == "id,bought_id,sell_date,sell_price\n"
        assert lines[5] == "5,5,2021-12-08,3.5\n"


def test_sell_product_existing_file_multiple_product():

    # test with existing 'sold' file and product quantity > 1
    init_test_bought_csv()
    init_test_sold_csv()

    sell_product("apple", date(2021, 12, 8), 3.5, 2, B_PATH, S_PATH)

    with open(S_PATH, "r") as file:
        lines = file.readlines()
        # check headers
        # skip bought_id 1 (expired apple) and bought_id 4 (apple already sold)
        # add apples with bought_id 5 and 6
        assert lines[0] == "id,bought_id,sell_date,sell_price\n"
        assert lines[5] == "5,5,2021-12-08,3.5\n"
        assert lines[6] == "6,6,2021-12-08,3.5\n"


def test_sell_product_existing_file_out_of_stock_single_product():
    # test whether sys.exit() gets invoked
    # when trying to buy a single product, which is not in stock
    # test with existing 'sold' file

    init_test_bought_csv()
    init_test_sold_csv()

    # If product to be sold is not in inventory,
    # sys.exit() gets called in main.py and raises SystemExit error.
    # Below test checks for this exception,
    # by wrapping the call that should invoke SystemExit exception in a 'with' block
    # This test passes as long as the exception is thrown
    with pytest.raises(SystemExit) as wrapped_exception:
        sell_product("mango", date(2021, 12, 8), 3.5, 1, B_PATH, S_PATH)
        assert wrapped_exception.type == SystemExit


def test_sell_product_existing_file_out_of_stock_multiple_products():
    # test whether sys.exit() gets invoked
    # when trying to buy multiple products, of which two are not in stock
    # test with existing 'sold' file

    init_test_bought_csv()
    init_test_sold_csv()

    with pytest.raises(SystemExit) as wrapped_exception:
        sell_product("pear", date(2021, 12, 8), 3.5, 3, B_PATH, S_PATH)
        assert wrapped_exception.type == SystemExit

    # also test whether 'sell' call has still logged
    # the one product (out of three that was in stock as sold
    with open(S_PATH, "r") as file:
        lines = file.readlines()
        assert lines[0] == "id,bought_id,sell_date,sell_price\n"
        assert lines[5] == "5,8,2021-12-08,3.5\n"


############################################################################


def test_get_report_with_profit():

    init_test_bought_csv()
    init_test_sold_csv()
    ledger = Ledger(B_PATH, S_PATH)

    # get_report takes as arguments:
    # a report_month as dateobject,
    # a report function (get_profit_day, get_revenue_day, get_product_sales)
    # and a product name if report_func is set to 'get_product_sales')
    # and returns a df

    test_df = get_report(date(2021, 12, 1), ledger.get_revenue_day)
    test_df_aslist = test_df[1].tolist()

    assert isinstance((test_df), pd.DataFrame)
    assert len(test_df_aslist) == 31
    assert test_df_aslist == [
        0,0,0,0,4.5,2.5,1,0,
        0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0,0,
        0,0,0,0,0,0,0
        ]  # fmt: skip
