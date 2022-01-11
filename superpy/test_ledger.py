from datetime import date
import pytest
from example_products import *
from ledger import Product, Ledger
import os


@pytest.fixture(autouse=True)
def run_after_tests():
    # Fixture to execute after each test is run:
    # creates test csv files before running each function
    # and cleanes them up afterwards

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
# testing initialization of Product and Ledger classes


def test_Product_initialization():

    apple1 = Product(14, "apple", date(2021, 12, 12), 1.2, date(2022, 1, 1))

    assert isinstance(apple1, Product) is True
    assert apple1.bought_id == 14
    assert apple1.name == "apple"
    assert apple1.buy_date == date(2021, 12, 12)
    assert apple1.buy_price == 1.2
    assert apple1.expiration == date(2022, 1, 1)
    assert apple1.sold_id == None
    assert apple1.sell_date == None
    assert apple1.sell_price == None


def test_Ledger_initialization():

    ledger = Ledger(B_PATH, S_PATH)

    # check if ledger is an instance of class Ledger
    assert isinstance(ledger, Ledger) is True

    # check if ledger has same number of instances as there are products in bought.csv
    assert len(ledger.products) == 9

    # check if product instances are created correctly,
    # and if sold, this information is added
    assert ledger.products[0].bought_id == 1
    assert ledger.products[0].sold_id == None
    assert ledger.products[5].name == "apple"
    assert ledger.products[6].sold_id == 2


def test_Ledger_initialization_no_bought_products():
    # checks whether invoking Ledger class gives error
    # when no products have been bought yet

    os.remove(B_PATH)
    os.remove(S_PATH)

    with pytest.raises(SystemExit) as wrapped_exception:
        Ledger(B_PATH, S_PATH)
        assert wrapped_exception.type == SystemExit


def test_Ledger_initialization_no_sold_products():
    # checks whether a ledger still gets created
    # when no products have been sold yet

    os.remove(S_PATH)
    ledger = Ledger(B_PATH, S_PATH)

    assert isinstance(ledger, Ledger) is True
    assert len(ledger.products) == 9


############################################################################
# testing the methods within Ledger class


def test_show_product():

    ledger = Ledger(B_PATH, S_PATH)
    product = ledger.show_product(1)

    assert isinstance(product, Product)
    assert product.bought_id == 1
    assert product.name == "apple"
    assert product.buy_date == date(2021, 11, 1)


def test_show_inventory_no_sold_products():
    # tests functionality if no items have been sold
    # (test_sold.csv does not exists)
    # test if the inventory of certain date does not hold
    # items which are expired or not yet bought:

    os.remove(S_PATH)
    ledger = Ledger(B_PATH, S_PATH)

    df, headers = ledger.show_inventory(date(2021, 12, 31))
    df_aslist = df.values.tolist()

    # skip expired product (bought_id 1, apple)
    # exclude product not yet bought (bought_id 8, banana)
    assert headers == ["id", "product", "buy_date", "buy_price", "expiration"]
    assert df_aslist[0] == [2, "pear", "2021-12-04", 2.0, "2042-01-01"]
    assert df_aslist[1] == [3, "banana", "2021-12-05", 2.1, "2042-01-01"]
    assert df_aslist[2] == [4, "apple", "2021-12-06", 2.0, "2042-01-01"]
    assert df_aslist[3] == [5, "apple", "2021-12-06", 2.3, "2042-01-01"]
    assert df_aslist[4] == [6, "apple", "2021-12-06", 2.0, "2042-01-01"]
    assert df_aslist[5] == [7, "pear", "2021-12-07", 2.0, "2042-01-01"]
    assert df_aslist[6] == [9, "banana", "2021-12-31", 3.2, "2042-01-01"]

    assert len(df_aslist) == 7


def test_show_inventory_with_bought_and_sold_products():
    # test if the inventory of certain date does not hold items
    # that are already sold, expired or not yet bought

    ledger = Ledger(B_PATH, S_PATH)
    df, headers = ledger.show_inventory(date(2021, 12, 31))
    df_aslist = df.values.tolist()

    # skip expired products: bought_id 1, apple
    # exclude products already sold: bought_id 4, apple // 2, pear // 3, banana // 7, pear
    # exclude product not yet bought: bought_id 8, banana
    assert headers == ["id", "product", "buy_date", "buy_price", "expiration"]
    assert df_aslist[0] == [5, "apple", "2021-12-06", 2.3, "2042-01-01"]
    assert df_aslist[1] == [6, "apple", "2021-12-06", 2.0, "2042-01-01"]
    assert df_aslist[2] == [9, "banana", "2021-12-31", 3.2, "2042-01-01"]

    assert len(df_aslist) == 3


def test_get_revenue_no_sold_products():
    # tests whether revenue is always 0
    # if no products have been sold (sold.csv does not exist)

    os.remove(S_PATH)
    ledger = Ledger(B_PATH, S_PATH)

    # the valid_month & valid_year functions in the track_date module will
    # convert month and year input on commandline
    # into full date (input 2021-12 --> output 2021-12-1)
    # but the get_revenue method only looks at month and year parts.
    assert ledger.get_revenue_day(date(2021, 12, 5)) == 0
    assert ledger.get_revenue_month(date(2021, 12, 1)) == 0
    assert ledger.get_revenue_year(date(2021, 1, 1)) == 0


def test_get_revenue_day_with_sold_products():
    # revenue is sum of sell_prices on input date

    ledger = Ledger(B_PATH, S_PATH)
    assert ledger.get_revenue_day(date(2021, 12, 5)) == 4.5
    assert ledger.get_revenue_month(date(2021, 12, 1)) == 8
    assert ledger.get_revenue_year(date(2021, 1, 1)) == 8


def test_get_profit_no_sold_items():
    # when no items are sold:
    # profit = 0 - expenses (all products bought on/within a given date or time period)

    os.remove(S_PATH)
    ledger = Ledger(B_PATH, S_PATH)

    assert ledger.get_profit_day(date(2021, 12, 6)) == -6.3
    assert ledger.get_profit_month(date(2021, 12, 1)) == -15.6
    assert ledger.get_profit_year(date(2021, 1, 1)) == -18.1


def test_get_profit_with_sold_items():

    ledger = Ledger(B_PATH, S_PATH)

    # profit on 2021-12-6 = revenue(2.5) - expenses (6.3)
    assert ledger.get_profit_day(date(2021, 12, 6)) == -3.8
    # profit in 2021-12 = revenue(8) - expenses (15.6)
    assert ledger.get_profit_month(date(2021, 12, 1)) == -7.6
    # profit in 2012 = revenue(8) - expenses (18.1)
    assert ledger.get_profit_year(date(2021, 12, 1)) == -10.1
