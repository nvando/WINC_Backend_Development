import sys
import csv
from pathlib import Path
from datetime import datetime

BOUGHT_PATH = Path("bought.csv")
SOLD_PATH = Path("sold.csv")

#######################################################################################
# function for logging bought and sold products into csv files:


def create_csv(path, headings):

    with open(path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headings)
        print(f"Created {path}")


def buy_product(product_name, buy_date, buy_price, expiration_date, quantity, b_path=BOUGHT_PATH):
    # give csv to create/open as argument instead of hard-coded
    # to make it easier to test functiom

    # create bought.csv if it doesn't exists and add header
    if not b_path.is_file():
        create_csv(
            b_path,
            [
                "id",
                "product",
                "buy_date",
                "buy_price",
                "expiration",
            ],
        )

    # open with r to obtain highest/last id,
    # then when file pointer is at end of file
    # append products with writerow() to csv
    with open(b_path, "r+", newline="") as file:
        reader = csv.reader(file)
        writer = csv.writer(file)

        next(reader)  # skip column names
        try:
            # compare 'int' version of each id (key=lambda row: int(row[0]),
            # then choose the row with largest id (max),
            # then obtain id (row[0]), convert to integer and ad 1
            id = int(max(reader, key=lambda row: int(row[0]))[0]) + 1  #
        except ValueError as error:  # if file does not have rows yet, set id to 1
            id = 1

        while quantity >= 1:  # quantity argument determines no of rows written in bought.csv
            writer.writerow(
                [
                    id,
                    product_name,
                    buy_date,
                    round(buy_price, 2),
                    expiration_date,
                ]
            )
            print(f"Logged {product_name} in 'bought.csv' with product_id {id}")
            quantity -= 1
            id += 1


def sell_product(
    product_name, sell_date, sell_price, quantity, b_path=BOUGHT_PATH, s_path=SOLD_PATH
):

    # create a file if it does not exists and add headers
    if not s_path.is_file():
        print("creating file")
        create_csv(s_path, ["id", "bought_id", "sell_date", "sell_price"])

    # check if item is in store and assign bought_id to sold item
    with open(s_path, "r+", newline="") as sold_file, open(b_path, "r", newline="") as bought_file:
        sold_reader = csv.reader(sold_file)
        bought_reader = csv.reader(bought_file)
        sold_writer = csv.writer(sold_file)

        while quantity >= 1:
            for row in sold_reader:
                assigned_ids = [row[1] for row in sold_reader]  # list of items already sold

            # retrieve id from bought.csv of a similar product,
            # if that product has not already been sold (assigned a sold_id)
            # and has not been expired yet
            bought_id = None  # set flag to check later on whether bought_id could be assigned
            for row in bought_reader:
                if (
                    row[1] == product_name  # product type is the same
                    and row[0] not in assigned_ids  # product not sold
                    and datetime.strptime(row[4], "%Y-%m-%d").date()
                    >= sell_date  # product not expired
                ):
                    bought_id = row[0]  # assign bought id
                    break
            if bought_id is None:  # no similar item (not sold/expired) found in bought.csv
                if quantity == 1:
                    print("Error: product not in stock")
                elif quantity > 1:
                    print("Error: remaining product(s) not in stock")
                sys.exit()

            # retrieve highest/last id in sold.csv
            sold_file.seek(0)  # return pointer to beginning of sold.csv,
            next(sold_reader)  # skip column names
            try:
                id = int(max(sold_reader, key=lambda row: int(row[0]))[0]) + 1
            except ValueError as error:  # if no products are entered
                id = 1

            # append product with writerow() to sold.csv
            sold_writer.writerow([id, bought_id, sell_date, sell_price])
            print(f"Added {product_name} to 'sold.csv' with id {id} and bought_id {bought_id}")
            quantity -= 1
