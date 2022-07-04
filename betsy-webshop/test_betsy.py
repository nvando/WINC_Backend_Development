from main import *
from peewee import *
import pytest


# @pytest.fixture(autouse=True)
# def run_before_tests():

create_test_data()


def test_search():
    # test if search returns the products
    # with the word 'cotton' in the name or description

    products = search("cotton")
    assert type(products) == list
    assert len(products) == 2
    assert (
        ("cotton" in product.name.lower() or "cotton" in product.description.lower())
        for product in products
    )


def test_list_user_products():
    # test if all 2 products are listed of user with id 5

    products = list_user_products(5)
    assert type(products) == list
    assert len(products) == 2
    assert any((product.name == "Hand Painted Denim Jeans") for product in products)
    assert any((product.name == "HedgeHog Sweater") for product in products)


def test_list_products_per_tag():
    # list the two product with tag 'summer' (tag_id 6)

    products = list_products_per_tag(6)
    assert type(products) == list
    assert len(products) == 2
    for product in products:
        # generator expression
        assert any((tag.name == "summer") for tag in product.tags)
    assert any((product.name == "Organic Cotton Legging") for product in products)
    assert any((product.name == "Panama Summer Hat") for product in products)


def test_add_product_to_catalog():

    new_product = add_product_to_catalog(
        3,
        "Anime Hoody Unisex",
        "Anime Unisex Hoody from Ghibli Studio, Japanese, with Spirit gods.",
        4250,
    )
    new_product_id = new_product.id

    new_product = Product.get(Product.id == new_product_id)
    assert new_product.name == "Anime Hoody Unisex"
    assert (
        new_product.description
        == "Anime Unisex Hoody from Ghibli Studio, Japanese, with Spirit gods."
    )
    assert new_product.price_in_cents == 4250
    assert new_product.sold_by_user.id == 3
    assert new_product.quantity == 1


def test_remove_product():

    with pytest.raises(DoesNotExist):
        assert remove_product(5) == Product.get(Product.id == 5)


def test_update_stock():

    update_stock(1, 100)
    assert Product.get(Product.id == 1).quantity == 100


def test_purchase_product():

    transaction = purchase_product(1, 5, 2)
    transaction_id = transaction.id

    transaction = Transaction.get(Transaction.id == transaction_id)
    assert transaction.user.id == 5
    assert transaction.product.id == 1
    assert transaction.quantity == 2


def test_purchase_product_insufficient_stock():
    # check if trying to buy more products then in stock, returns a None

    assert purchase_product(1, 5, 200) == None
