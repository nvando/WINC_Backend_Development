import models
from peewee import *
from typing import List
import datetime

__winc_id__ = "286787689e9849969c326ee41d8c53c4"
__human_name__ = "Peewee ORM"


def cheapest_dish():
    """You want to get food on a budget
    Query the database to retrieve the cheapest dish available
    """

    query = models.Dish.select().order_by(models.Dish.price_in_cents.asc()).limit(1)
    cheapest_dish = query[0]
    return cheapest_dish


def vegetarian_dishes() -> List[models.Dish]:

    """You'd like to know what vegetarian dishes are available

    Query the database to return a list of dishes that contain only
    vegetarian ingredients.
    """

    vega_dishes = []
    for dish in models.Dish.select():
        print(dish.name)
        only_vega_ingredients = True
        for ingredient in dish.ingredients:
            if ingredient.is_vegetarian is False:
                only_vega_ingredients = False

        if only_vega_ingredients is True:
            vega_dishes.append(dish)
            print("appending ", dish.name)

    return vega_dishes


def best_average_rating() -> models.Restaurant:
    """You want to know what restaurant is best

    Query the database to retrieve the restaurant that has the highest
    rating on average
    """

    best_rest = (
        models.Restaurant.select(
            models.Restaurant, fn.AVG(models.Rating.rating).alias("avg_rating")
        )
        .join(models.Rating, JOIN.INNER)
        .group_by(models.Restaurant.name)
        .order_by(SQL("avg_rating").desc())
    )

    for restaurant in best_rest:
        print(restaurant.name, restaurant.avg_rating)

    return best_rest[0]


def add_rating_to_restaurant() -> None:
    """After visiting a restaurant, you want to leave a rating

    Select the first restaurant in the dataset and add a rating
    """

    first_rest = models.Restaurant.get()
    models.Rating.create(rating=8, restaurant=first_rest, comment="new comment")
    query = (
        models.Restaurant.select(
            models.Restaurant.name, models.Rating.rating, models.Rating.comment
        )
        .join(models.Rating)
        .where(models.Restaurant.name == first_rest.name)
    )

    # printing all the ratings of this restaurant to see if comment has been added
    for row in query:
        print(row.name, "- rating: ", row.rating.rating, row.rating.comment)


def dinner_date_possible() -> List[models.Restaurant]:
    """You have asked someone out on a dinner date, but where to go?

    You want to eat at around 19:00 and your date is vegan.
    Query a list of restaurants that account for these constraints.
    """

    # find dishes with only vegan ingredients
    vegan_dishes = []
    for dish in models.Dish.select():
        only_vegan_ingredients = True
        for ingredient in dish.ingredients:
            if ingredient.is_vegan is False:
                only_vegan_ingredients = False

        if only_vegan_ingredients is True:
            vegan_dishes.append(dish.name)

    print("vegan_dishes: ", vegan_dishes)

    # the restaurant is open between 18:00 and 20:00
    required_opening = datetime.time(18, 00, 00)
    required_closing = datetime.time(20, 00, 00)

    # the restaurant that has at least one dish that has only vegan ingredients
    # the restaurant needs to be open between 'required_opening' and 'required_closing'
    query = (
        models.Restaurant.select(models.Restaurant)
        .join(models.Dish, on=(models.Dish.served_at == models.Restaurant.id))
        .where(
            (
                models.Dish.name.in_(vegan_dishes)
                & (models.Restaurant.opening_time <= required_opening)
                & (models.Restaurant.closing_time >= required_closing)
            )
        )
    )

    restaurant_options = [restaurant for restaurant in query]
    return restaurant_options


def add_dish_to_menu() -> models.Dish:
    """You have created a new dish for your restaurant and want to add it to the menu

    The dish you create must at the very least contain 'cheese'.
    You do not know which ingredients are in the database, but you must not
    create ingredients that already exist in the database. You may create
    new ingredients however.
    Return your newly created dish
    """

    # new dish data:
    new_dish = ("pizza hawai", 3, 1200)
    new_dish_ingredients = (
        ("flour", (True, True, False)),
        ("tomato", (True, True, True)),
        ("cheese", (False, True, True)),
        ("ham", (False, False, True)),
        ("pineapple", (True, True, True)),
    )

    # create new dish with Dish model
    models.Dish.create(name=new_dish[0], served_at=new_dish[1], price_in_cents=new_dish[2])

    # add ingredients if not already created
    for name, diet in new_dish_ingredients:
        ing, created = models.Ingredient.get_or_create(
            name=name, is_vegan=diet[0], is_vegetarian=diet[1], is_glutenfree=diet[2]
        )
        if created is True:
            print("added ", ing.name)
        else:
            print(ing.name, " already in database")

    # add ingredient_data to new dish data
    dish = models.Dish.get(models.Dish.name == new_dish[0])
    for ingredient in new_dish_ingredients:
        ing = models.Ingredient.get(models.Ingredient.name == ingredient[0])
        dish.ingredients.add(ing)

    return models.Dish.get(models.Dish.name == new_dish[0])
    return None
