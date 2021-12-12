from datetime import date
from main import *
import os
from pathlib import Path
import pytest
import pandas


# sold product items for test file 'bought.csv'
TEST_ITEMS_BOUGHT = [
    "id,product,buy_date,buy_price,expiration",
    "1,apple,2021-12-01,2.5,2021-01-01",  # example expired product
    "2,pear,2021-12-04,2.0,2022-01-01",
    "3,banana,2021-12-05,2.1,2022-01-01",
    "4,apple,2021-12-06,2.0,2022-01-01",
    "5,apple,2021-12-06,2.33,2022-01-01",
    "6,apple,2021-12-06,2.0,2022-01-01",
    "7,pear,2021-12-07,2.0,2022-01-01",
    "8,pear,2022-01-01,2.56,2023-01-01",  # example product bought before inventory date
    "9,banana,2021-12-31,3.2,2022-01-01",
]

# sold product items for test file 'sold.csv'
TEST_ITEMS_SOLD = [
    "id,bought_id,sell_date,sell_price",
    "1,2,2021-12-05,2.0",  # pear 1
    "2,7,2021-12-05,2.5",  # pear 2
    "3,3,2021-12-06,2.5",  # banana 1
    "4,4,2021-12-07,1.0",  # apple 1
]


############################################################################
# initialization functions to creat dummy csv files
# to test functions of the superpy module


def init_test_bought_csv():

    # initialize 'dummy' csv-file to test with 10 rows
    with open("test_bought.csv", "w") as file:
        # writer = csv.writer(file)
        for line in TEST_ITEMS_BOUGHT:
            file.write(line)
            file.write("\n")


def init_test_sold_csv():

    # initialize 'dummy' csv-file to test with 10 rows
    with open("test_sold.csv", "w") as file:
        # writer = csv.writer(file)
        for line in TEST_ITEMS_SOLD:
            file.write(line)
            file.write("\n")


############################################################################
# tests for date manipulation functions of main.py in the superpy module


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
# test the create csv function of main.py in the superpy module


def test_create_csv():

    create_csv("test", ["heading1", "heading2"])
    assert os.path.isfile("test")

    with open("test", "r") as file:
        line = file.readline()

        assert line == "heading1,heading2\n"

    os.remove("test")


############################################################################
# tests for the buy product function of main.py within the superpy module


def test_buy_product_new_file_single_product():

    # test with no existing file and product quantity = 1
    b_path = Path("test_bought.csv")
    buy_product("apple", date(2021, 10, 1), 2.3, date(2021, 12, 12), 1, b_path)
    with open(b_path, "r") as file:
        lines = file.readlines()
        assert lines[0] == "id,product,buy_date,buy_price,expiration\n"
        assert lines[1] == "1,apple,2021-10-01,2.3,2021-12-12\n"
    os.remove(b_path)


def test_buy_product_new_file_multiple_products():
    # test with no exiting file and product quantity = 3
    b_path = Path("test_bought.csv")
    buy_product("apple", date(2021, 10, 1), 2.3, date(2021, 12, 12), 3, b_path)
    with open(b_path, "r") as file:
        lines = file.readlines()
        assert lines[0] == "id,product,buy_date,buy_price,expiration\n"
        assert lines[1] == "1,apple,2021-10-01,2.3,2021-12-12\n"
        assert lines[2] == "2,apple,2021-10-01,2.3,2021-12-12\n"
        assert lines[3] == "3,apple,2021-10-01,2.3,2021-12-12\n"
    os.remove(b_path)


def test_buy_product_existing_file_single_product():

    init_test_bought_csv()

    b_path = Path("test_bought.csv")
    buy_product("apple", date(2021, 10, 1), 2.3, date(2021, 12, 12), 1, b_path)

    # test whether product is addes as row 10, after existing product on row 9
    with open(b_path, "r") as file:
        lines = file.readlines()
        assert lines[9] == "9,banana,2021-12-31,3.2,2022-01-01\n"
        assert lines[10] == "10,apple,2021-10-01,2.3,2021-12-12\n"

    os.remove(b_path)


def test_buy_product_existing_file_multiple_products():

    # initialize 'dummy' csv-file to test with 10 rows
    init_test_bought_csv()

    # test if multiple rows are added after existing row 9
    # if quantity > 1
    b_path = Path("test_bought.csv")
    buy_product("apple", date(2021, 10, 1), 2.3, date(2021, 12, 12), 3, b_path)

    with open(b_path, "r") as file:
        lines = file.readlines()
        assert lines[9] == "9,banana,2021-12-31,3.2,2022-01-01\n"
        assert lines[10] == "10,apple,2021-10-01,2.3,2021-12-12\n"
        assert lines[11] == "11,apple,2021-10-01,2.3,2021-12-12\n"
        assert lines[12] == "12,apple,2021-10-01,2.3,2021-12-12\n"

    os.remove(b_path)


############################################################################
# tests for the sell product function of main.py within the superpy module


def test_sell_product_new_file_single_product():

    # test with no existing file and product quantity = 1
    init_test_bought_csv()
    s_path = Path("test_sold.csv")
    b_path = Path("test_bought.csv")

    sell_product("apple", date(2021, 12, 8), 3.5, 1, b_path, s_path)

    # test whether product gets added to inventory
    # and are not expired
    with open(s_path, "r") as file:
        lines = file.readlines()
        # check header
        assert lines[0] == "id,bought_id,sell_date,sell_price\n"
        # skip bought_id 1, expired apple, add 2nd apple with bought_id 4
        assert lines[1] == "1,4,2021-12-08,3.5\n"

    os.remove(s_path)
    os.remove(b_path)


def test_sell_product_new_file_multiple_products():
    # test with no exiting file and product quantity = 3

    init_test_bought_csv()
    s_path = Path("test_sold.csv")
    b_path = Path("test_bought.csv")

    sell_product("apple", date(2021, 12, 8), 3.5, 3, b_path, s_path)

    # test whether product gets added to inventory
    # and are not expired
    with open(s_path, "r") as file:
        lines = file.readlines()
        # check headers
        # skip bought_id 1, expired apple, add 2nd apple with bought_id 4
        assert lines[0] == "id,bought_id,sell_date,sell_price\n"
        assert lines[1] == "1,4,2021-12-08,3.5\n"
        assert lines[2] == "2,5,2021-12-08,3.5\n"
        assert lines[3] == "3,6,2021-12-08,3.5\n"

    os.remove(s_path)
    os.remove(b_path)


def test_sell_product_existing_file_single_product():

    # test with no existing file and product quantity = 1
    init_test_bought_csv()
    init_test_sold_csv()
    s_path = Path("test_sold.csv")
    b_path = Path("test_bought.csv")

    sell_product("apple", date(2021, 12, 8), 3.5, 1, b_path, s_path)

    # test whether product gets added to inventory
    # and is not expired
    # and has not ben sold already
    with open(s_path, "r") as file:
        lines = file.readlines()
        # check headers
        # skip bought_id 1 (expired apple) and bought_id 4 (apple already sold)
        # add apple with bought_id 5
        assert lines[0] == "id,bought_id,sell_date,sell_price\n"
        assert lines[5] == "5,5,2021-12-08,3.5\n"

    os.remove(s_path)
    os.remove(b_path)


def test_sell_product_existing_file_multiple_product():

    # test with existing 'sold' file and product quantity > 1
    init_test_bought_csv()
    init_test_sold_csv()
    s_path = Path("test_sold.csv")
    b_path = Path("test_bought.csv")

    sell_product("apple", date(2021, 12, 8), 3.5, 2, b_path, s_path)

    with open(s_path, "r") as file:
        lines = file.readlines()
        # check headers
        # skip bought_id 1 (expired apple) and bought_id 4 (apple already sold)
        # add apples with bought_id 5 and 6
        assert lines[0] == "id,bought_id,sell_date,sell_price\n"
        assert lines[5] == "5,5,2021-12-08,3.5\n"
        assert lines[6] == "6,6,2021-12-08,3.5\n"

    os.remove(s_path)
    os.remove(b_path)


def test_sell_product_existing_file_out_of_stock_single_product():
    # test whether sys.exit() gets invoked
    # when trying to buy a single product, which is not in stock
    # test with existing 'sold' file

    init_test_bought_csv()
    init_test_sold_csv()
    s_path = Path("test_sold.csv")
    b_path = Path("test_bought.csv")

    # If product to be sold is not in inventory,
    # sys.exit() gets called in main.py and raises SystemExit error.
    # Below test checks for this exception,
    # by wrapping the call that should invoke SystemExit exception in a 'with' block
    # This test passes as long as the exception is thrown
    with pytest.raises(SystemExit) as wrapped_exception:
        sell_product("mango", date(2021, 12, 8), 3.5, 1, b_path, s_path)
        assert wrapped_exception.type == SystemExit

    os.remove(b_path)
    os.remove(s_path)


def test_sell_product_existing_file_out_of_stock_multiple_products():
    # test whether sys.exit() gets invoked
    # when trying to buy multiple products, of which two are not in stock
    # test with existing 'sold' file

    init_test_bought_csv()
    init_test_sold_csv()
    s_path = Path("test_sold.csv")
    b_path = Path("test_bought.csv")

    with pytest.raises(SystemExit) as wrapped_exception:
        sell_product("pear", date(2021, 12, 8), 3.5, 3, b_path, s_path)
        assert wrapped_exception.type == SystemExit

    # also test whether 'sell' call has still logged
    # the one product (out of three that was in stock as sold
    with open(s_path, "r") as file:
        lines = file.readlines()
        assert lines[0] == "id,bought_id,sell_date,sell_price\n"
        assert lines[5] == "5,8,2021-12-08,3.5\n"

    os.remove(b_path)
    os.remove(s_path)


############################################################################
# tests for the sell product function of main.py within the superpy module


def test_show_inventory_no_bought_products():

    s_path = Path("test_sold.csv")
    b_path = Path("test_bought.csv")

    with pytest.raises(SystemExit) as wrapped_exception:
        show_inventory(date(2021, 12, 9), b_path, s_path)
        assert wrapped_exception.type == SystemExit


def test_show_inventory_no_sold_products():

    init_test_bought_csv()
    b_path = Path("test_bought.csv")
    s_path = Path("test_sold.csv")

    # test if the inventory of certain date does not hold
    # item which are expired or not yet bought
    df, headers = show_inventory(date(2021, 12, 31), b_path, s_path)
    df_aslist = df.values.tolist()

    # skip expired product (bought_id 1, apple)
    # exclude product not yet bought (bought_id 8, banana)
    assert headers == ["id", "product", "buy_date", "buy_price", "expiration"]
    assert df_aslist[0] == ["2", "pear", "2021-12-04", "2.0", "2022-01-01"]
    assert df_aslist[1] == ["3", "banana", "2021-12-05", "2.1", "2022-01-01"]
    assert df_aslist[2] == ["4", "apple", "2021-12-06", "2.0", "2022-01-01"]
    assert df_aslist[3] == ["5", "apple", "2021-12-06", "2.33", "2022-01-01"]
    assert df_aslist[4] == ["6", "apple", "2021-12-06", "2.0", "2022-01-01"]
    assert df_aslist[5] == ["7", "pear", "2021-12-07", "2.0", "2022-01-01"]
    assert df_aslist[6] == ["9", "banana", "2021-12-31", "3.2", "2022-01-01"]
    assert len(df_aslist) == 7

    os.remove(b_path)


def test_show_inventory():
    # test if the inventory of certain date does not hold items
    # that are already sold, expired or not yet bought

    init_test_bought_csv()
    init_test_sold_csv()
    b_path = Path("test_bought.csv")
    s_path = Path("test_sold.csv")

    df, headers = show_inventory(date(2021, 12, 31), b_path, s_path)
    df_aslist = df.values.tolist()

    # skip expired products: bought_id 1, apple
    # exclude products already sold: bought_id 4, apple // 2, pear // 3, banana // 7, pear
    # exclude product not yet bought: bought_id 8, banana
    assert headers == ["id", "product", "buy_date", "buy_price", "expiration"]
    assert df_aslist[0] == ["5", "apple", "2021-12-06", "2.33", "2022-01-01"]
    assert df_aslist[1] == ["6", "apple", "2021-12-06", "2.0", "2022-01-01"]
    assert df_aslist[2] == ["9", "banana", "2021-12-31", "3.2", "2022-01-01"]
    assert len(df_aslist) == 3

    os.remove(b_path)
    os.remove(s_path)
