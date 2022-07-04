from models import *
import peewee
import os

if os.path.exists("test_data.db"):
    os.remove("test_data.db")

db = peewee.SqliteDatabase("test_data.db")

dishes_data = (
    ("pasta carbonara", 1, 1500),
    ("pasta napolitana", 3, 1300),
    ("pasta pollo", 2, 1400),
    ("pizza margarita", 1, 1100),
    ("risotto vegatariana", 2, 1000),
)

ingredients_data = (
    ("chicken", (False, False, True)),
    ("potato", (True, True, True)),
    ("pasta", (True, True, False)),
    ("cheese", (False, True, True)),
    ("pinenut", (True, True, True)),
    ("tomato", (True, True, True)),
    ("pork", (False, False, True)),
    ("flour", (True, True, False)),
    ("risotto", (True, True, True)),
)

dish_ingredients = (
    ("pasta carbonara", ("pasta", "pork", "cheese")),
    ("pasta napolitana", ("pasta", "tomato", "pinenut")),
    ("pasta pollo", ("pasta", "chicken", "tomato")),
    ("pizza margarita", ("flour", "tomato", "cheese")),
    ("risotto vegatariana", ("risotto", "tomato", "potato", "pinenut")),
)

restaurant_data = (
    ("Pinokio", 1980, "18:00", "20:00"),
    ("Florencia", 2015, "17:00", "23:00"),
    ("Casa di Pasta", 2010, "12:00", "18:00"),
)

rating_data = (
    (
        1,
        7,
    ),
    (
        1,
        6,
    ),
    (
        1,
        4,
    ),
    (
        2,
        7,
    ),
    (
        2,
        8,
    ),
    (
        2,
        7,
    ),
    (
        2,
        8,
    ),
    (
        2,
        9,
    ),
    (
        3,
        6,
    ),
    (
        3,
        7,
    ),
    (
        3,
        7,
    ),
    (
        3,
        7,
    ),
    (
        3,
        6,
    ),
    (
        3,
        6,
    ),
)


def populate_test_data():

    db.create_tables([Ingredient, Restaurant, Dish, Rating, DishIngredient], safe=False)

    for name, diet in ingredients_data:
        Ingredient.create(name=name, is_vegan=diet[0], is_vegetarian=diet[1], is_glutenfree=diet[2])

    for dish in dishes_data:
        Dish.create(name=dish[0], served_at=dish[1], price_in_cents=dish[2])

    for dish_name, ingredients in dish_ingredients:
        dish = Dish.get(Dish.name == dish_name)
        print(dish.name)
        for ingredient in ingredients:

            ing = Ingredient.get(Ingredient.name == ingredient)
            dish.ingredients.add(ing)

    for restaurant in restaurant_data:
        Restaurant.create(
            name=restaurant[0],
            open_since=restaurant[1],
            opening_time=restaurant[2],
            closing_time=restaurant[3],
        )

    for rating in rating_data:
        Rating.create(
            restaurant=rating[0],
            rating=rating[1],
        )
