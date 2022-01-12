# example products bought for test file 'bought.csv'
from pathlib import Path

TEST_ITEMS_BOUGHT = [
    "id,product,buy_date,buy_price,expiration",
    "1,apple,2021-11-01,2.5,2021-01-01",  # example expired product
    "2,pear,2021-12-04,2.0,2042-01-01",  # expiration set far in future so testing stays valid for 20yrs
    "3,banana,2021-12-05,2.1,2042-01-01",
    "4,apple,2021-12-06,2.0,2042-01-01",
    "5,apple,2021-12-06,2.3,2042-01-01",
    "6,apple,2021-12-06,2.0,2042-01-01",
    "7,pear,2021-12-07,2.0,2042-01-01",
    "8,pear,2022-01-01,2.5,2042-01-01",  # example product bought before inventory date
    "9,banana,2021-12-31,3.2,2042-01-01",
]

# example sold products for test file 'sold.csv'
TEST_ITEMS_SOLD = [
    "id,bought_id,sell_date,sell_price",
    "1,2,2021-12-05,2.0",  # pear 1
    "2,7,2021-12-05,2.5",  # pear 2
    "3,3,2021-12-06,2.5",  # banana 1
    "4,4,2021-12-07,1.0",  # apple 1
]

B_PATH = Path("test_bought.csv")
S_PATH = Path("test_sold.csv")


############################################################################
# initialization functions to creat dummy csv files
# needed to test the functions of the superpy module


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
