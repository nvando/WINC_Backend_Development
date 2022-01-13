import argparse
from track_date import valid_date, valid_month, valid_year


def create_super_parser():
    """ 
    This function creates the argument parser 'super_parser'.
    The following commands are added as subparsers: 
        buy /sell / show-product / show-inventory / report-total / report-overtime / 
        show-date / set-date / advance-time
    Each sub-command int turn has it's own arguments,
    which are either required or have a default values set. 
    The arguments for each subcommand can be checked for type.
    The date arguments are validated through the valid_date function,imported from the track_date module
    The arguments are then parsed with parse_args and returned as object attributes"""
   

    super_parser = argparse.ArgumentParser(description="Keep track of supermarket inventory")
    subparsers = super_parser.add_subparsers(dest="command", help="Sub-commands")

    # subparser for buy command
    buy_parser = subparsers.add_parser(
        "buy",
        help="""Logs a product into the inventory,
        enter product name, price,
        buy date, expiration date and quantity""",
    )
    buy_parser.add_argument(
        "--product",
        required=True,
        help="Enter product name",
    )
    buy_parser.add_argument(
        "--buy-date",
        required=False,
        default="today",
        type=valid_date,
        help="Enter buy date in format YYYY-MM-DD, default is 'today'",
    )
    buy_parser.add_argument(
        "--price",
        required=True,
        type=float,
        help="enter price as float with 1 decimal",
    )
    buy_parser.add_argument(
        "--expiration",
        required=True,
        type=valid_date,
        help="Enter expiration date in format YYYY-MM-DD",
    )
    buy_parser.add_argument(
        "--quantity",
        required=False,
        default=1,
        type=int,
        help="Enter number of bougth products which the same price and expiration date, default = 1",
    )

    # subparser for sell command,
    sell_parser = subparsers.add_parser(
        "sell",
        help="""log a pruduct as sold.
        Enter product name, price,
        sell date and quantity""",
    )
    sell_parser.add_argument(
        "--product",
        required=True,
        help="Enter product name",
    )
    sell_parser.add_argument(
        "--sell-date",
        required=False,
        default="today",
        type=valid_date,
        help="Enter buy date in format YYYY-MM-DD, default is 'today'",
    )
    sell_parser.add_argument(
        "--price",
        required=True,
        type=float,
        help="enter price as float, will be rounded to two decimals",
    )
    sell_parser.add_argument(
        "--quantity",
        required=False,
        default=1,
        type=int,
        help="Enter number of products sold on the same date for the same price, default = 1",
    )

    # --------------------------------------------------------------------------------------------------------------------

    # subparser for show-product command
    product_parser = subparsers.add_parser("show-product")
    product_parser.add_argument(
        "product_id",
        type=int,
        help="Enter the id assigned to the product when bought (bought_id)",
    )


    # subparser for show-inventory command
    inventory_parser = subparsers.add_parser("show-inventory", help="reports on inventory")
    inventory_parser.add_argument(
        "date",
        type=valid_date,
        help="Enter report date as today, yesterday or as format YYYY-MM-DD, default = 'today",
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
        help="""report total revenue or profit for a given day, month or year""",
    )
    report_total_parser.add_argument(
        "type_of_report",  # argparse won't allow use of word 'report-type'
        choices=["revenue", "profit"],
        help="choose type of report. Then choose and set reporting period with --date, --month or --year",
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
    
    # subparser for report-overtime command
    report_overtime = subparsers.add_parser(
        "report-overtime",
        help="""plots daily revenue or profit over given month""",
    )
    report_overtime.add_argument(
        "type_of_report",  # argparse won't allow use of word 'report-type'
        choices=["revenue", "profit", "revenue-profit", "product-sales"],
        help="choose which type of income to plot",
    )

    report_overtime.add_argument(
        "report_month", type=valid_month, help="Enter month in format YYYY-MM"
    )

    report_overtime.add_argument(
        "--product", help="Enter the name of product you want to see sales of"
    )

    report_overtime.add_argument(
        "--to-excel",
        action="store_true",  #  sets arg.to-excel as True:  can be used to enable a feature
        help="Save plot data as table in as Excel spreadsheet",
    )

    report_overtime.add_argument(
        "--to-pdf",
        action="store_true",  #  sets arg.to-excel as True: can be used to enable a feature
        help="Save figure as PDF",
    )

    report_overtime.add_argument(
        "--to-jpeg",
        action="store_true",  #  sets arg.to-excel as True: can be used to enable a feature
        help="Save figure as JPEG image",
    )

    # ---------------------------------------------------------------------------------------------------------------------------

 
    # subparser for advance-date command
    advance_parser = subparsers.add_parser(
        "advance-time",
    )
    advance_parser.add_argument(
        "no_of_days",
        type=int,
        help="Advance system time a certain number of days",
    )

    # subparser for set-date command
    set_parser = subparsers.add_parser(
        "set-date",
    )
    set_parser.add_argument(
        "date_to_set",
        type=valid_date,
        help="Enter date in format YYYY-MM-DD",
    )
    # subparser for show-date command
    subparsers.add_parser("show-date")

    # ---------------------------------------------------------------------------------------------------------------------------

    return super_parser.parse_args()
