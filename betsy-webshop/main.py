__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

from models import *
from data_generator import create_test_data
from peewee import *
from tabulate import tabulate


def search(term):
    # Search product names and descriptions based on a term (case-insensitive)

    query = Product.select().where(
        (Product.name.contains(term)) | (Product.description.contains(term))
    )

    if query.exists():
        for product in query:
            print("ID:", product.id, product.name, " - ", product.description)
    else:
        print(f"no {term} found in products")

    return [product for product in query]


def list_user_addresses(user_id):
    # List postal and billing address for a given user

    query = (
        User.select(User, Postal, Billing)
        .join(Postal)
        .switch(User)
        .join(Billing, JOIN.LEFT_OUTER)
        .where(User.id == user_id)
    )

    for user in query:
        postal_address = f"{user.postal.street}, {user.postal.postcode}, {user.postal.city}"
        if user.postal.same_as_billing is True:
            billing_address = "same as postal"
        else:
            billing_address = f"{user.billing.street}, {user.billing.postcode}, {user.billing.city}"

        print(
            tabulate(
                [[user.id, user.username, user.fullname, postal_address, billing_address]],
                headers=["id", "username", "fullname", "streetaddress", "billingadress"],
            )
        )

    return [user for user in query]


def list_user_products(user_id):
    # View the products of a given user

    query = Product.select(User, Product).join(User).where(User.id == user_id)

    table = []
    for product in query:
        table.append(
            [product.sold_by_user.username, product.name, product.price_in_cents, product.quantity]
        )

    print(
        tabulate(table, headers=["user_id", "product name", "price in cents", "quantity in store"])
    )
    # print(
    #     tabulate(
    #         [[user.id, user.username,]],
    #         headers=["id", "username", "fullname", "streetaddress", "billingadress"],
    #     )

    return [product for product in query]


def list_products_per_tag(tag_id):

    try:
        tag = Tag.get(Tag.id == tag_id)
        print("tag: ", tag.name)
    except DoesNotExist:
        print("Not a valid tag_id")

    print("Product(s):")
    for product in tag.products:
        print(product.name)

    return [product for product in tag.products]


def add_product_to_catalog(user_id, product):
    ...


def update_stock(product_id, new_quantity):
    ...


def purchase_product(product_id, buyer_id, quantity):
    ...


def remove_product(product_id):
    ...


if __name__ == "__main__":
    create_test_data()
    print("test data created")
    # term = input("Enter search term: ")
    # search(term)
    # user_id = input("Enter user_id: ")
    # list_user_addresses(user_id)
    # list_user_products(user_id)
    tag_id = input("Enter tag_id: ")
    list_products_per_tag(tag_id)
