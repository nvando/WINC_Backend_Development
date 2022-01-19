import csv
from datetime import datetime
import pandas as pd
import sys


class Product:
    def __init__(
        self,
        bought_id,
        product_name,
        buy_date,
        buy_price,
        expiration,
    ):
        self.bought_id = bought_id
        self.name = product_name
        self.buy_date = buy_date
        self.buy_price = buy_price
        self.expiration = expiration
        self.sold_id = None
        self.sell_date = None
        self.sell_price = None


class Ledger:
    # creates list instances of all products bought and sold
    # on which methods can be called that return revenue and profit
    # on a certain date or over a period of time.

    def __init__(self, b_path, s_path):
        self.products = []
        self.__add_products(b_path, s_path)

    def __add_products(
        self, b_path, s_path
    ):  # defining private method so it won't be used outside class

        # quit program when bought.csv has not been created
        if not b_path.is_file():
            print("No products bought yet: inventory is empty")
            sys.exit()

        # convert each row in bought_csv file to a product instance
        with open(b_path, "r") as file:
            bought_reader = csv.reader(file)
            next(bought_reader)
            for row in bought_reader:
                self.products.append(
                    Product(
                        int(row[0]),
                        row[1],
                        datetime.strptime(row[2], "%Y-%m-%d").date(),
                        float(row[3]),
                        datetime.strptime(row[4], "%Y-%m-%d").date(),
                    )
                )

        # check if item has been sold and add sold_id, sell price and date
        if s_path.is_file():
            with open(s_path, "r") as file:
                sold_reader = csv.reader(file)
                next(sold_reader)
                for row in sold_reader:
                    bought_id = int(row[1])
                    for product in self.products:
                        if bought_id == product.bought_id:
                            product.sold_id = int(row[0])
                            product.sell_date = datetime.strptime(row[2], "%Y-%m-%d").date()
                            product.sell_price = float(row[3])
                            break

    def show_product(self, bought_id):
        for product in self.products:
            if product.bought_id == bought_id:
                return product

    def show_inventory(self, inventory_date):
        # add products to inventory if:
        # it had been bought before the inventory date,
        # has not been sold or sold after the inventory date
        # has not yet been sold and has not expired

        inventory = []
        for product in self.products:
            if (
                product.buy_date <= inventory_date
                and (product.sold_id is None or product.sell_date > inventory_date)
                and product.expiration >= inventory_date
            ):
                inventory.append(
                    [
                        product.bought_id,
                        product.name,
                        product.buy_date.strftime("%Y-%m-%d"),  # converting so easier to test
                        product.buy_price,
                        product.expiration.strftime("%Y-%m-%d"),
                    ]
                )

        if len(inventory) != 0:
            df = pd.DataFrame(inventory)
            headers = ["id", "product", "buy_date", "buy_price", "expiration"]
            df.columns = headers
        else:
            print(f"Inventory empty on {inventory_date}")
            sys.exit()

        return df, headers

    def get_revenue_day(self, report_date):

        sell_prices = [
            product.sell_price
            for product in self.products
            if not product.sell_date is None and product.sell_date == report_date
        ]

        return sum(sell_prices)

    def get_revenue_month(self, report_date):

        sell_prices = [
            product.sell_price
            for product in self.products
            if not product.sell_date is None
            and product.sell_date.month == report_date.month
            and product.sell_date.year == report_date.year
        ]

        return sum(sell_prices)

    def get_revenue_year(self, report_date):

        sell_prices = [
            product.sell_price
            for product in self.products
            if not product.sell_date is None and product.sell_date.year == report_date.year
        ]

        return sum(sell_prices)

    def get_profit_day(self, report_date):

        buy_prices = [
            product.buy_price for product in self.products if product.buy_date == report_date
        ]

        # profit =  revenue - expenses
        return round(self.get_revenue_day(report_date) - sum(buy_prices), 2)

    def get_profit_month(self, report_date):

        buy_prices = [
            product.buy_price
            for product in self.products
            if product.buy_date.month == report_date.month
            and product.buy_date.year == report_date.year
        ]

        # profit =  revenue - expenses
        return round(self.get_revenue_month(report_date) - sum(buy_prices), 2)

    def get_profit_year(self, report_date):

        buy_prices = [
            product.buy_price
            for product in self.products
            if product.buy_date.year == report_date.year
        ]

        # profit =  revenue - expenses
        return round(self.get_revenue_year(report_date) - sum(buy_prices), 2)

    def get_product_sales(self, report_date, product):

        no_sold_products = 0

        for sold_product in self.products:
            if product == sold_product.name and report_date == sold_product.sell_date:
                no_sold_products += 1

        return no_sold_products
