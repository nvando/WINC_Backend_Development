from peewee import *
import re

database = SqliteDatabase("test_data.db")


class BaseModel(Model):
    class Meta:
        database = database


class Tag(BaseModel):
    name = TextField(unique=True)  # tags should not be duplicated


class Postal(BaseModel):
    street = CharField()
    postcode = CharField(constraints=[Check("length(postcode)<=7 AND length(postcode)>=6")])
    city = TextField()
    same_as_billing = BooleanField(default=True)


class Billing(BaseModel):
    street = CharField(null=True)
    postcode = CharField(null=True)
    city = TextField(null=True)


class User(BaseModel):
    username = CharField()
    fullname = TextField()
    postal = ForeignKeyField(Postal)
    billing = ForeignKeyField(Billing, null=True)


class Product(BaseModel):
    name = CharField(index=True)
    description = CharField(index=True)
    tags = ManyToManyField(Tag, backref="products")  # facilitates search and categorization
    price_in_cents = IntegerField(
        constraints=[Check("price_in_cents > 0")]
    )  # pricing in cents prevents rounding errors
    sold_by_user = ForeignKeyField(User, index=True)
    quantity = IntegerField()


class Transaction(BaseModel):
    # link a buyer with a purchased product and a quantity of purchased items
    user = ForeignKeyField(User)  # only users can purchase products
    product = ForeignKeyField(Product)
    quantity = IntegerField()


ProductTags = Product.tags.get_through_model()
