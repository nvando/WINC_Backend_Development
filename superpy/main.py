# Library imports
import sys
from tabulate import tabulate
import matplotlib.pyplot as plt
import pandas as pd


# application imports
import parsers
from track_date import TODAY, set_date, advance_time
from buysell import *
from ledger import *
from plotreports import *


# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# create super_parser by running the imported create_super_parser function
args = parsers.create_super_parser()

###########################################################################################################


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

###########################################################################################################

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

##################################################################################################

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

#######################################################################################################

if args.command == "report-total":
    # create ledger (list) of all products and
    # call on it the get_revenue or get_profit method
    # for the specified date or period

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

######################################################################################################

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
        if args.product is not None:
            df = get_report(args.report_month, ledger.get_product_sales, args.product)
            df.columns = ["Day", f"{args.product} sales"]
        else:
            print(
                "Error: Missing required argument '--product'.\nplease enter '--product' followed by the product you want to report on"
            )
            sys.exit()

    print(
        tabulate(
            df,
            headers=df.columns,
            tablefmt="psql",
            showindex=False,
        )
    )

    fig, ax = plot_df(df, args.report_month)

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

############################################################################################################################

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
