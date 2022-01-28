# Library imports
import sys
from tabulate import tabulate
import matplotlib.pyplot as plt
import pandas as pd


# application imports
import parsers
from trackdate import TODAY, set_date, change_date
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
        args.buydate,
        args.price,
        args.expiration,
        args.quantity,
    )

if args.command == "sell":
    sell_product(
        args.product,
        args.selldate,
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
    if args.to_csv:

        filename = f"Inventory on {args.date}.csv"
        df.to_csv(REPORTS_PATH / filename, index=False)
        print(f"Inventory saved as '{filename}' in Superpy/reports folder")

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
        print("\nPRODUCT EXPIRED")
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
            revenue = ledger.get_revenue_day(args.day)
            print(f"Total revenue on {args.day}: {revenue}")
        elif args.month:
            revenue = ledger.get_revenue_month(args.month)
            month = args.month.strftime("%B")
            print(f"Total revenue in {month} {args.month.year}: {revenue}")
        elif args.year:
            revenue = ledger.get_revenue_year(args.year)
            print(f"Total revenue in {args.year.year}: {revenue}")
        else:
            print(
                """Set reporting period with --day, --month or --year, 
                then enter date in format (YYYY-MM-DD),(YYYY-MM) or (YYYY) respectively"""
            )

    if args.type_of_report == "profit":
        if args.day:
            profit = ledger.get_profit_day(args.day)
            print(f"Total profit on {args.day}: {profit}")
        elif args.month:
            profit = ledger.get_profit_month(args.month)
            month = args.month.strftime("%B")
            print(f"Total profit in {month} {args.month.year}: {profit}")
        elif args.year:
            profit = ledger.get_profit_year(args.year)
            print(f"Total profit in {args.year.year}: {profit}")
        else:
            print(
                """Set reporting period with --day, --month or --year, 
                then enter date in format (YYYY-MM-DD),(YYYY-MM) or (YYYY) respectively"""
            )

######################################################################################################

if args.command == "report-period":
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
            df.columns = ["Day", f"Number of {args.product}s sold"]
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

    if args.product is None:
        filename_no_extension = f"{args.type_of_report.capitalize()} for {args.report_month.strftime('%B')} {args.report_month.year}"
    else:
        filename_no_extension = f"{args.product.capitalize()} sales for {args.report_month.strftime('%B')} {args.report_month.year}"

    if args.to_pdf:
        filename = filename_no_extension + ".pdf"
        fig.savefig(REPORTS_PATH / filename)
        print(f"Figure saved as '{filename}' in Superpy/reports folder")

    if args.to_jpeg:
        filename = filename_no_extension + ".jpeg"
        fig.savefig(REPORTS_PATH / filename)
        print(f"Figure saved as '{filename}' in Superpy/reports folder")

    if args.to_csv:
        filename = filename_no_extension + ".csv"
        df.to_csv(REPORTS_PATH / filename, index=False)
        print(f"Data saved in '{filename}' in Superpy/reports folder")

    if args.to_excel:
        filename = filename_no_extension + ".xlsx"
        df.to_excel(REPORTS_PATH / filename, index=False)
        print(f"Table saved as '{filename}' in Superpy/reports folder")

    plt.show()

############################################################################################################################

if args.command == "show-date":
    print(f"This program has today's date stored as {TODAY}")

if args.command == "change-date":
    TODAY = change_date(TODAY, args.no_of_days)
    print(f"This program's date has been changed to {TODAY}")

if args.command == "set-date":
    TODAY = set_date(args.date_to_set)
    print(f"This program's date has been set to {args.date_to_set}")
