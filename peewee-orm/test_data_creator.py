from models import *
import peewee

db = peewee.SqliteDatabase("test_data.db")

dishes_data = (
    ("pasta carbonara", "Pinokio", 1500),
    ("pasta napolitana", "Casa di Pasta", 1300),
    ("pasta pollo", "Florencia", 1400),
    ("pizza margarita", "Pinokio", 1100),
    ("risotto vegatariana", "Florencia", 1000),
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


def populate_test_data():
    db.create_tables([Ingredient, Restaurant, Dish, Rating, DishIngredient])

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
            print(dish.name, ing.is_vegan)

    # favorite_data = (
    #     ('huey', ['whine']),
    #     ('mickey', ['purr']),
    #     ('zaizee', ['meow', 'purr']))
    # for username, favorites in favorite_data:
    #     user = User.get(User.username == username)
    #     for content in favorites:
    #         tweet = Tweet.get(Tweet.content == content)
    #         Favorite.create(user=user, tweet=tweet)
