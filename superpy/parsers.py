import argparse
from track_date import valid_date


def create_super_parser():
    # this function creates subparsers for the commands buy, sell and report
    # and for show, set and advance date
    # Each sub-command then has it's own arguments,
    # which are either required or have a default value
    # The arguments of each can be checked for type.
    # The date arguments are validated by the valid_date function,
    # imported from the track_date module

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
    # subparser for report command
    report_parser = subparsers.add_parser(
        "report",
        help="""reports on inventory or revenue""",
    )
    report_parser.add_argument(
        "type_of_report",  # argparse won't allow use of word 'report-type'
        choices=["inventory", "revenue"],
        help="choose type of report",
    )
    report_parser.add_argument(
        "date_of_report",
        type=valid_date,
        help="Enter report date in format YYYY-MM-DD, default is 'today",
    )

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
    subparsers.add_parser(
        "show-date",
    )

    return super_parser.parse_args()
