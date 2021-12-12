# Imports
import csv
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd
from tabulate import tabulate
import parsers
from track_date import TODAY
import sys

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


BOUGHT_PATH = Path("bought.csv")
SOLD_PATH = Path("sold.csv")

# set current date as today when opening file for first time,
# and write it to today.csv
# otherwise read today.csv to retrieve current date


def set_date(date_obj):

    with open("today.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(["todays_date", date_obj])


def advance_time(today, no_of_days):
    # moved defining of global TODAY into main()
    # as easier to test outside this function

    today += timedelta(days=(int(no_of_days)))
    set_date(today)
    return today


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
            id = int(max(reader, key=lambda row: int(row[0]))[0]) + 1
        except ValueError as error:  # if file does not have rows yet
            id = 1

        while quantity >= 1:  # quantity entered determines no of rows
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

    # assign bought_id to sold item and check if item is in store
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
                    row[1] == product_name
                    and row[0] not in assigned_ids
                    and datetime.strptime(row[4], "%Y-%m-%d").date() >= sell_date
                ):
                    bought_id = row[0]
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


def show_inventory(inventory_date, b_path=BOUGHT_PATH, s_path=SOLD_PATH):

    # quit program when bought.csv has not been created
    if not b_path.is_file():
        print("No products bought yet: inventory is empty")
        sys.exit()

    # if sold.csv not yet created set list of sold_id's to empty
    elif not s_path.is_file():
        sold_ids = []

    # grab id's of products that have been sold
    # up to inventory date
    else:
        with open(s_path, "r", newline="") as sold_file:
            sold_reader = csv.reader(sold_file)

            next(sold_reader)  # skip headers
            sold_ids = [
                row[1]
                for row in sold_reader
                if datetime.strptime(row[2], "%Y-%m-%d").date() <= inventory_date
            ]

    # add product from bought.csv to inventory
    # if product has not been sold
    # if it had already been bought on the inventory date
    # if it has not expired
    with open(b_path, "r", newline="") as bought_file:

        bought_reader = csv.reader(bought_file)
        headers = next(bought_reader)

        inventory = []
        for row in bought_reader:
            if (
                row[0] not in sold_ids
                and datetime.strptime(row[2], "%Y-%m-%d").date() <= inventory_date
                and datetime.strptime(row[4], "%Y-%m-%d").date() >= inventory_date
            ):
                inventory.append(row)
        df = pd.DataFrame(inventory)

    # return df and print outside function in at call-site
    # (arg.command if statement)
    # so that it is possible to verify dataframe with testing
    # otherwise printing would be a side effect of this fucntion
    # and hard to test

    return df, headers


# ---------------------------------------------------------------------------------------------------


def main():
    global TODAY

    # create super_parser by running the imported create parser function
    args = parsers.create_super_parser()

    if args.command == "buy":
        buy_product(
            args.product,
            args.buy_date,
            args.price,
            args.expiration,
            args.quantity,
        )

    if args.command == "sell":
        sell_product(
            args.product,
            args.sell_date,
            args.price,
            args.quantity,
        )

    if args.command == "report":
        if args.type_of_report == "inventory":
            df, headers = show_inventory(args.date_of_report)
            print(
                tabulate(
                    df,
                    headers=headers,
                    tablefmt="psql",
                    showindex=False,
                )
            )

    if args.command == "show-date":
        print(f"The system has today's date stored as {TODAY}")

    if args.command == "advance-time":
        TODAY = advance_time(TODAY, args.no_of_days)
        print(f"The program's date has been changed to {TODAY}")

    if args.command == "set-date":
        set_date(args.date_to_set)
        print(f"The program's date has been set to {TODAY}")


if __name__ == "__main__":
    main()
