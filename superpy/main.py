# Imports
import sys
import csv
from datetime import datetime, timedelta, date
import calendar
from pathlib import Path
from tabulate import tabulate
import matplotlib.pyplot as plt
import pandas as pd


import parsers
from track_date import TODAY
from ledger import Ledger


# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


BOUGHT_PATH = Path("bought.csv")
SOLD_PATH = Path("sold.csv")
REPORTS_PATH = Path("reports")  # create folder for storing excel and pdf reports, if not exists
REPORTS_PATH.mkdir(parents=True, exist_ok=True)


#######################################################################################


def set_date(date_obj):

    with open("today.csv", "w+") as file:
        writer = csv.writer(file)
        writer.writerow(["todays_date", date_obj])


def advance_time(today, no_of_days):
    # moved defining of global TODAY into ()
    # as easier to test outside this function

    today += timedelta(days=(int(no_of_days)))
    set_date(today)
    return today


#######################################################################################


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


def get_report(report_month, report_func, product=None):

    no_days_in_month = calendar.monthrange(report_month.year, report_month.month)[1]

    # for each day in month
    # calculate profit or revenue (output)
    daily_output = []
    for day in range(1, no_days_in_month + 1):
        if product is None:
            output = report_func(date(report_month.year, report_month.month, day))
        else:
            output = report_func(date(report_month.year, report_month.month, day), product)
        daily_output.append([day, output])

    df = pd.DataFrame(daily_output)

    return df


def df_to_plot(df, overview_month):

    if len(df.columns) == 2:
        y = str(df.columns[1]).lower()
    else:
        y = f"{df.columns[1]} and {df.columns[2]}".lower()

    fig, ax = plt.subplots()

    df.plot(
        kind="line",
        ax=ax,
        alpha=0.450,
        x="Day",
        ylabel="Euro",
        title=f"Showing daily {y} for {overview_month.strftime('%B')} {overview_month.year}",
    )

    return fig, ax


# ---------------------------------------------------------------------------------------------------

# everything below this statement won't be executed when file is imported
# for instance when importing main in test_file

if __name__ == "__main__":
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

    if args.command == "show-inventory":
        ledger = Ledger(BOUGHT_PATH, SOLD_PATH)
        df, headers = ledger.show_inventory(args.date)
        print(
            tabulate(
                df,
                headers=headers,
                tablefmt="psql",
                showindex=False,
            )
        )
        if args.to_excel:

            filename = f"Inventory on {args.date}.xlsx"
            df.to_excel(REPORTS_PATH / filename, index=False)
            print(f"Inventory saved as '{filename}' in Superpy/reports folder")

    if args.command == "report-total":
        # create ledger of all products and
        # call revenue or profit method for specified date or period
        ledger = Ledger(BOUGHT_PATH, SOLD_PATH)

        if args.type_of_report == "revenue":
            if args.day:
                print(ledger.get_revenue_day(args.day))
            elif args.month:
                print(ledger.get_revenue_month(args.month))
            elif args.year:
                print(ledger.get_revenue_year(args.year))
            else:
                print(
                    """Set reporting period with --day, --month or --year, 
                    then enter date in format (YYYY-MM-DD),(YYYY-MM) or (YYYY) respectively"""
                )

        if args.type_of_report == "profit":
            if args.day:
                print(ledger.get_profit_day(args.day))
            elif args.month:
                print(ledger.get_profit_month(args.month))
            elif args.year:
                print(ledger.get_profit_year(args.year))
            else:
                print(
                    """Set reporting period with --day, --month or --year, 
                    then enter date in format (YYYY-MM-DD),(YYYY-MM) or (YYYY) respectively"""
                )

    if args.command == "show-product":
        product = Ledger(BOUGHT_PATH, SOLD_PATH).show_product(args.product_id)
        print(
            f"\n Product ID: {product.bought_id}\n",
            f"Product name: {product.name}\n",
            f"Product bought on: {product.buy_date}\n",
            f"Product bought for: ${product.buy_price}\n",
            f"Product expires on: {product.expiration}",
        )
        if product.sold_id is not None:
            print(
                f"\n Product sold on: {product.sell_date}\n",
                f"Product sold for: ${product.sell_price}\n",
            )
        elif product.expiration < TODAY:
            print("PRODUCT EXPIRED")
        else:
            print("\n Product not sold yet\n")

    if args.command == "report-overtime":
        ledger = Ledger(BOUGHT_PATH, SOLD_PATH)
        if args.type_of_report == "revenue":
            df = get_report(args.report_month, ledger.get_revenue_day)
            df.columns = ["Day", "Revenue"]
        elif args.type_of_report == "profit":
            df = get_report(args.report_month, ledger.get_profit_day)
            df.columns = ["Day", "Profit"]
        elif args.type_of_report == "revenue-profit":
            df_revenue = get_report(args.report_month, ledger.get_revenue_day)
            df_profit = get_report(args.report_month, ledger.get_profit_day)
            df = pd.concat([df_revenue, df_profit.iloc[:, 1]], axis=1)
            df.columns = ["Day", "Revenue", "Profit"]
        elif args.type_of_report == "product-sales":
            if args.product is None:
                print(
                    "Error: Missing required argument '--product'. Please enter '--product' followed by the product you want to report on"
                )
                sys.exit()
            else:
                df = get_report(args.report_month, ledger.get_product_sales, args.product)
                df.columns = ["Day", f"{args.product} sales"]

        print(
            tabulate(
                df,
                headers=df.columns,
                tablefmt="psql",
                showindex=False,
            )
        )

        fig, ax = df_to_plot(df, args.report_month)

        if args.to_pdf:
            filename = f"{args.type_of_report} for {args.report_month.strftime('%B')} {args.report_month.year}.pdf"
            fig.savefig(REPORTS_PATH / filename)
            print(f"Figure saved as '{filename}' in Superpy/reports folder")

        if args.to_jpeg:
            filename = f"{args.type_of_report} for {args.report_month.strftime('%B')} {args.report_month.year}.jpg"
            fig.savefig(REPORTS_PATH / filename)
            print(f"Figure saved as '{filename}' in Superpy/reports folder")

        if args.to_excel:
            filename = f"{args.type_of_report} for {args.report_month.strftime('%B')} {args.report_month.year}.xlsx"
            df.to_excel(REPORTS_PATH / filename, index=False)
            print(f"Table saved as '{filename}' in Superpy/reports folder")

        plt.show()

    if args.command == "show-date":
        print(f"The system has today's date stored as {TODAY}")

    if args.command == "advance-time":
        TODAY = advance_time(TODAY, args.no_of_days)
        print(f"The program's date has been changed to {TODAY}")

    if args.command == "set-date":
        TODAY = set_date(args.date_to_set)
        print(f"The program's date has been set to {args.date_to_set}")


# three technical features:
# testable code
# making code testable by leaving print statements outside functions
#   (for instance, return df in show_inventory method
#   and print he df outside function in at call-site,
#   so that it is possible to verify dataframe with testing,
#   otherwise printing would be a side effect of this function and hard to test)
# and by not hardcoding the file paths into the function but giving them as parameters
# so we can test the fucntions with a dummy FileDescriptor

# creating subparsers:
# adding subparsers so that for each command we can define which named arguments are required.
# For instance with the 'buy' command,
# one is promted to always enter product_name, buy_date, buy_price and expiration date.
# each argument can also be tested seperately for being of the right type,
# which makes it easy to test whether dates are entered correctly
# and above all, makes sure the csv date files don't hold faulty dates or data fields

# creating a class Product and a collection class Ledgers:
# The class Ledger has a 'get_product' method which loads the info the csv files
# and creates a product instance for each row.
# These product instances are then loaded into an instance list using the collection class Ledger.
# On this list one can invoke the class methods such as show revenue or profit.
# why useful??


# still to do:
# load inventorys into csv or pdf's
# another feature?
