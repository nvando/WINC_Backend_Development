__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

from models import *
from data_generator import create_test_data
from peewee import *
from tabulate import tabulate
from fuzzywuzzy import fuzz


def search(search_term):
    # Search product names and descriptions
    # based on a term (case-insensitive)

    search_results = []

    # first check if a product name or descriptions contains exact search term
    query = Product.select().where(
        (Product.name.contains(search_term)) | (Product.description.contains(search_term))
    )

    if query.exists():
        for product in query:
            print("Found product:", product.id, product.name, " - ", product.description)
            search_results.append(product)
        return search_results

    # else use fuzzy search with a similarity percentage > 70
    else:
        query = Product.select()
        for product in query:
            name_ratio = fuzz.partial_ratio(search_term.lower(), product.name.lower())
            descr_ratio = fuzz.partial_ratio(search_term.lower(), product.description.lower())
            if name_ratio > 70 or descr_ratio > 70:
                search_results.append(product)
                print("Found product:", product.id, product.name, " - ", product.description)
        if len(search_results) >= 1:
            return search_results
        else:
            print("No matches found")
            return None


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


def add_product_to_catalog(user_id, product_name, product_descr, product_price, quantity=1):

    new_product = Product.create(
        name=product_name,
        description=product_descr,
        price_in_cents=product_price,
        sold_by_user=user_id,
        quantity=quantity,
    )

    print(f"Created {product_name} with product id {new_product.id}")

    return new_product


def update_stock(product_id, new_quantity):

    product = Product.get(Product.id == product_id)
    product.quantity = new_quantity
    product.save()


def purchase_product(product_id, buyer_id, quantity):

    # check if sufficient stock
    product = Product.get(Product.id == product_id)
    if quantity > product.quantity:
        print(
            f"Not enough producs in stock, maximum number of items to be purchased is {product.quantity}"
        )
        return None

    else:
        new_quantity = product.quantity - quantity
        update_stock(product_id, new_quantity)
        transaction = Transaction.create(user=buyer_id, product=product_id, quantity=quantity)
        return transaction


def remove_product(product_id):

    product = Product.get(Product.id == product_id)
    product_name = product.name
    sold_by_user = product.sold_by_user
    user = User.get(User.id == sold_by_user).username

    product.delete_instance()
    print(f"Removed {product_name} from catalog of user {user}")
