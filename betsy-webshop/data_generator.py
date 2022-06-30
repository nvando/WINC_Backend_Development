from models import *
from peewee import *
import os

# start with a fresh database when running script
if os.path.exists("test_data.db"):
    os.remove("test_data.db")

database = SqliteDatabase("test_data.db")

tag_data = (
    "mens",
    "womens",
    "kids",
    "jeans",
    "winter",
    "summer",
    "sale",
    "new_arrivals",
    "sweater",
)
product_data = (
    (
        "Organic Cotton Legging",
        "Slim fitted legging with elastic waistband, made from organic cotton",
        2000,
        ["womens", "summer", "sale"],
        50,
        1,
    ),
    (
        "Leather Tote Bag",
        "Handmade women tote bag is produced of Eco-Friendly VEGAN leather for a high-end look.",
        5500,
        ["womens", "new_arrivals"],
        15,
        1,
    ),
    (
        "Crochet Baby Shoes",
        "A pair of cute silver coloured crochet baby booties that are gender neutral and made from a soft premium acrylic yarn",
        1675,
        ["kids", "winter"],
        5,
        2,
    ),
    (
        "Panama Summer Hat",
        "Panama hat in Ivory is your new must have summer accessory to compliment any outfit. Made in a classic tan colour and featuring an embroidered ribbon",
        2995,
        ["mens", "sale", "summer"],
        30,
        4,
    ),
    (
        "Hand Painted Denim Jeans",
        "Upcycled denim jeans with tattoo style snakes",
        12900,
        ["jeans", "womens", "new_arrivals"],
        25,
        5,
    ),
    (
        "HedgeHog Sweater",
        "Sweatshirts of the Highest Quality cotton and polyester for softness and comfort, available in a variety of colors",
        2900,
        ["sweater", "womens", "sale"],
        10,
        5,
    ),
)


postal_address_data = (
    ("Bachstraat 111", "1015 RZ", "Amsterdam", False),
    ("Mozartstraat 6", "6661 JJ", "Arnhem", True),
    ("Burgermeester Roosstraat 212", "3011 CA", "Rotterdam", True),
    ("Ploegstraat 10", "1014 KB", "Amsterdam", False),
    ("Janskerkhof 4", "3562 JN", "Utrecht", True),
)

billing_address_data = (
    ("Lilly Lowlands", "Plantaanstraat 83", "1002 YH", "Amsterdam"),
    ("Truus Kraling", "Beukenplantsoen 12", "1087 XL", "Amsterdam"),
)

user_data = (
    (
        "Gingerlilly_1987",
        "Lilly Lowlands",
        1,
        1,
    ),
    (
        "HappyCat",
        "Catherine Moonshine",
        2,
        None,
    ),
    (
        "Crazy_Mabel",
        "Mabel Hitchkins",
        3,
        None,
    ),
    (
        "TreeLover4Ever",
        "Truus Kraling",
        4,
        2,
    ),
    (
        "Mishka_the_Fashioniska",
        "Mishka Svenski",
        5,
        None,
    ),
)


def create_test_data():

    database.create_tables(
        [
            Tag,
            Product,
            Postal,
            Billing,
            User,
            Transaction,
            ProductTags,
        ]
    )

    for tag in tag_data:
        Tag.create(name=tag)

    for postal_address in postal_address_data:
        Postal.create(
            street=postal_address[0],
            postcode=postal_address[1],
            city=postal_address[2],
            same_as_billing=postal_address[3],
        )

    for billing_address in billing_address_data:
        Billing.create(
            street=billing_address[0],
            postcode=billing_address[1],
            city=billing_address[2],
        )

    for user in user_data:
        User.create(username=user[0], fullname=user[1], postal=user[2], billing=user[3])

    for product_info in product_data:
        product = Product.create(
            name=product_info[0],
            description=product_info[1],
            price_in_cents=product_info[2],
            quantity=product_info[4],
            sold_by_user=product_info[5],
        )
        for tag in product_info[3]:
            tag_instance = Tag.get(Tag.name == tag)
            product.tags.add(tag_instance)
