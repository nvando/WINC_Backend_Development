# A user has a name, address data, and billing information.

from enum import unique
from peewee import *

database = SqliteDatabase(":memory:")


class BaseModel(Model):
    class Meta:
        database = database


class Tag(BaseModel):
    name = TextField(unique=True)  # tags should not be duplicated


class Product(BaseModel):
    name: CharField()
    description: CharField()
    tags = ManyToManyField(Tag)
    price_in_cents: IntegerField()
    in_stock: IntegerField()


class Postal(BaseModel):
    street_address: CharField()
    postcode: CharField()
    city: TextField()


class Billing(BaseModel):
    street_address: CharField()
    postcode: CharField()
    city: TextField()


class User(BaseModel):
    name = CharField()
    billing_address = ForeignKeyField(Postal)
    postal_address = ForeignKeyField(Billing)
    products = ManyToManyField(Product)


class Transaction(BaseModel):
    user: ForeignKeyField(User)
    product: ForeignKeyField(Product)
    quantity: IntegerField()


ProductTags = Product.tag.get_through_model()
UserProducts = User.products.get_through_model()


# Each user must be able to own a number of products.
# The products must have a name, a description, a price per unit, and a quantity describing the amount in stock.
# The price should be stored in a safe way; rounding errors should be impossible.
# In order to facilitate search and categorization, a product must have a number of descriptive tags.
# We want to be able to track the purchases made on the marketplace, therefore a transaction model must exist
# You can assume that only users can purchase goods
# The transaction model must link a buyer with a purchased product and a quantity of purchased items
