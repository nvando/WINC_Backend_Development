from pathlib import Path
from datetime import date
import calendar
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter, MaxNLocator


REPORTS_PATH = Path("reports")  # create folder for storing excel and pdf reports, if not exists
REPORTS_PATH.mkdir(parents=True, exist_ok=True)


##################################################################################################################
# functions that report on profit, revenue or productsales over time (monthly)


def get_report(report_month, report_method, product=None):
    # get_report takes as arguments:
    # a report_month as dateobject,
    # a report function: get_profit_day/get_revenue_day/get_product_sales on a ledger instance
    # a product name, only when report_method is set to 'get_product_sales'
    # and returns a df

    no_days_in_month = calendar.monthrange(report_month.year, report_month.month)[1]

    # for each day in month
    # calculate profit or revenue (output)
    daily_output = []
    for day in range(1, no_days_in_month + 1):
        if product is None:
            output = report_method(date(report_month.year, report_month.month, day))
        else:
            output = report_method(date(report_month.year, report_month.month, day), product)
        daily_output.append([day, output])

    df = pd.DataFrame(daily_output)

    return df


def plot_df(df, overview_month):

    # retrieve column names for use in plot title
    if len(df.columns) == 2:
        y_name = str(df.columns[1]).lower()
    else:
        y_name = f"{df.columns[1]} and {df.columns[2]}".lower()

    # determine title based on report-type
    if df.columns[1] == "Revenue" or df.columns[1] == "Profit":
        title = f"Showing daily {y_name} for {overview_month.strftime('%B')} {overview_month.year}"
    else:
        title = (
            f"Showing {y_name} per day for {overview_month.strftime('%B')} {overview_month.year}"
        )

    fig, ax = plt.subplots()

    ax.yaxis.set_major_formatter(FormatStrFormatter("%0.0f"))
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    df.plot(
        kind="line",
        ax=ax,
        alpha=0.450,
        x="Day",
        title=title,
    )

    return fig, ax
