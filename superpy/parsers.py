import argparse

from datetime import date
from track_date import valid_date, valid_month, valid_year


def create_super_parser():
    """
    This function creates the argument parser 'super_parser'.
    The following commands are added as subparsers:
        buy /sell / show-product / show-inventory / report-total / report-period /
        show-date / set-date / change-date
    Each sub-command int turn has it's own arguments,
    which are either required or have a default values set.
    The arguments for each subcommand can be checked for type.
    The date arguments are validated through the valid_date function,imported from the track_date module
    The arguments are then parsed with parse_args and returned as object attributes"""

    super_parser = argparse.ArgumentParser(
        description="""Keep track of the supermarket inventory.
        Log products as 'bought' or 'sold', 
        show information on a product or current inventory
        or report on profit and revenue 
        on certain days or over time period"""
    )
    subparsers = super_parser.add_subparsers(dest="command", help="Sub-commands")
    # Create subparsers for each main command,
    # as most of the commands necesarry for this program
    # (such as the 'buy', or 'report' command)
    # each require a unique set of arguments and
    # the subparsers allow's the program to distinguish between them

    # subparser for buy command
    buy_parser = subparsers.add_parser(
        "buy",
        help="""Log a product into the inventory.
        Follow with the required named-arguments product-name (--product), 
        price (--price) and expiration-date (--expiration).
        Buy-date (--buydate) is an optional argument, and will be set to the date 
        this program has stored as 'today' if ommited
        (check with the subcommand "show-date"). 
        Product quantity (--quantity) is also optional and set to 1 if ommited""",
    )

    # using named-arguments instead of positional arguments
    # as their order would be hard to remember if arguments were postional
    # With using named-arguments order does not matter,
    # and if arguments are required, the 'required' option is set to True

    buy_parser.add_argument(
        "--product",
        required=True,
        help="Enter the product name. Required argument",
    )
    buy_parser.add_argument(
        "--buydate",
        required=False,
        default="today",
        type=valid_date,
        help="""Enter buy-date in format YYYY-MM-DD. 
        Optional argument. Will be set to the date that 
        this program has stored as 'today' if ommited""",
    )
    buy_parser.add_argument(
        "--price",
        required=True,
        type=float,
        help="Enter price as float with 1 decimal. Required argument",
    )
    buy_parser.add_argument(
        "--expiration",
        required=True,
        type=valid_date,
        help="Enter expiration date in format YYYY-MM-DD. Required argument.",
    )
    buy_parser.add_argument(
        "--quantity",
        required=False,
        default=1,
        type=int,
        help="""Enter number of products bought on the same date,
        for the same price and with a similar expiration date. 
        Optional argument, default = 1.""",
    )

    # subparser for sell command,
    sell_parser = subparsers.add_parser(
        "sell",
        help="""Log a product as sold.
        Follow with the required named-arguments product-name (--product) 
        and sell-price (--price). Sell-date (--date) is an optional argument, 
        and will be set to the date this program has stored as 'today' if ommited.
        ('Today's date can be check with the subcommand "show-date") 
        Product quantity (--quantity) is also an optional argument and set to 1 if ommited.""",
    )
    sell_parser.add_argument(
        "--product",
        required=True,
        help="Enter product name. Required argument.",
    )
    sell_parser.add_argument(
        "--selldate",
        required=False,
        default="today",
        type=valid_date,
        help="""Enter sell-date in format YYYY-MM-DD.
        Optional argument. Will be set to the date that 
        this program has stored as 'today' if ommited.""",
    )
    sell_parser.add_argument(
        "--price",
        required=True,
        type=float,
        help="""Enter price as float, will be rounded to two decimals.
        Required argument.""",
    )
    sell_parser.add_argument(
        "--quantity",
        required=False,
        default=1,
        type=int,
        help=""""Enter number of products sold on the same date,
        for the same price. Optional argument, default = 1.""",
    )

    # --------------------------------------------------------------------------------------------------------------------

    # subparser for show-product command
    product_parser = subparsers.add_parser(
        "show-product",
        help="""Shows buy, sell and expiry data for product, given the product id.""",
    )
    product_parser.add_argument(
        "product_id",
        type=int,
        help="Enter the id assigned to the product when bought (bought_id)",
    )

    # subparser for show-inventory command
    inventory_parser = subparsers.add_parser(
        "show-inventory",
        help="""Shows inventory on a given date. 
        Enter inventory date as today, yesterday or as format YYYY-MM-DD, default = 'today'.
        The inventory can be exported to a csv or excel file, 
        by using the flags --to-csv or --to-excel respectively""",
    )
    inventory_parser.add_argument(
        "date",
        type=valid_date,
        help="Enter inventory date as today, yesterday or as format YYYY-MM-DD, default = 'today",
    )

    inventory_parser.add_argument(
        "--to-csv",
        action="store_true",  #  sets arg.csv as True: can be used to enable a feature
        help="Save inventory as csv-file",
    )
    inventory_parser.add_argument(
        "--to-excel",
        action="store_true",  #  sets arg.to-excel as True: can be used to enable a feature
        help="Save inventory as Excel spreadsheet",
    )

    # --------------------------------------------------------------------------------------------------------------------

    # subparser for report-total command
    report_total_parser = subparsers.add_parser(
        "report-total",
        help="""Report on total revenue or profit for a given day, month or year.
        Choose report-type (revenue or profit), then choose and set reporting period
        with named-arguments --date, --month or --year". If using --day, one can enter 
        'today', 'yesterday' or a date in format 'YYYY-MM-DD """,
    )
    report_total_parser.add_argument(
        "type_of_report",  # argparse won't allow use of word 'report-type'
        choices=["revenue", "profit"],
        help="""Choose type of report. 
        Then choose and set reporting period 
        with named arguments --day, --month or --year""",
    )

    report_total_parser.add_argument(
        "--day",
        type=valid_date,
        help="Enter report date as today, yesterday or as format YYYY-MM-DD, default = 'today",
    )

    report_total_parser.add_argument(
        "--month", type=valid_month, help="Enter report month in format YYYY-MM"
    )
    report_total_parser.add_argument(
        "--year", type=valid_year, help="Enter the year for which you want a report in format YYYY"
    )

    # --------------------------------------------------------------------------------------------------------------------

    # subparser for report-period command
    report_period = subparsers.add_parser(
        "report-period",
        help="""Plot daily revenue, profit or product-sales over a given month.
        Follow with month in format "YYYY-MM" and then by report-type:
        choose from 'revenue', 'profit', "revenue-profit' (both), 
        or 'product-sales. When report-type is product-sales, 
        use the named-argument --product to enter the product name.
        For all report types, 
        you can choose to save the output data to csv or excel file,
        or to the plot to a  jpeg or pdf file with the following flags:
        --to-csv --to-excel, --to-jpeg and --to-pdf""",
    )

    report_period.add_argument(
        "report_month", type=valid_month, help="Enter report-month in format YYYY-MM"
    )

    report_period.add_argument(
        "type_of_report",  # argparse won't allow use of word 'report-type'
        choices=["revenue", "profit", "revenue-profit", "product-sales"],
        help="""Choose which type of report to show. Choose from:
        'revenue', 'profit', 'revenue-profit', 'product-sales'""",
    )

    report_period.add_argument(
        "--product", help="Enter the name of product you want to see sales of"
    )

    report_period.add_argument(
        "--to-csv",
        action="store_true",  #  sets arg.to-excel as True:  can be used to enable a feature
        help="Save plot data in csv file",
    )

    report_period.add_argument(
        "--to-excel",
        action="store_true",  #  sets arg.to-excel as True:  can be used to enable a feature
        help="Save plot data as table in as Excel spreadsheet",
    )

    report_period.add_argument(
        "--to-pdf",
        action="store_true",  #  sets arg.to-excel as True: can be used to enable a feature
        help="Save figure as PDF",
    )

    report_period.add_argument(
        "--to-jpeg",
        action="store_true",  #  sets arg.to-excel as True: can be used to enable a feature
        help="Save figure as JPEG image",
    )

    # ---------------------------------------------------------------------------------------------------------------------------

    # subparser for advance-date command
    change_parser = subparsers.add_parser(
        "change-date",
        help="""Move the date that this program has stored as 'today'
        forward or backward by given numbers of days. 
        'Today' can be moved back using a negative number.""",
    )
    change_parser.add_argument(
        "no_of_days",
        type=int,
        help="Number of days the program's date will be moved forward or backward to.",
    )

    # subparser for set-date command
    set_parser = subparsers.add_parser(
        "set-date", help="""Set the date that this program has stored as 'today'"""
    )
    set_parser.add_argument(
        "date_to_set",
        type=date.fromisoformat,
        help="Enter date in format YYYY-MM-DD",
    )
    # subparser for show-date command
    subparsers.add_parser("show-date", help="Show the date that this program has set as 'today'")

    # ---------------------------------------------------------------------------------------------------------------------------

    return super_parser.parse_args()
