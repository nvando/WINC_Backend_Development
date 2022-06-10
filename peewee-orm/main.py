import models
from peewee import *
from typing import List

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
        only_vega_ingredients = True
        for ingredient in dish.ingredients:
            if ingredient.is_vegetarian is False:
                only_vega_ingredients = False

        if only_vega_ingredients is True:
            vega_dishes.append(dish)

    return vega_dishes


def best_average_rating() -> models.Restaurant:
    """You want to know what restaurant is best

    Query the database to retrieve the restaurant that has the highest
    rating on average
    """

    query = (
        models.Restaurant.select(
            models.Restaurant.name, fn.AVG(models.Rating.rating).alias("avg_rating")
        )
        .join(models.Rating, JOIN.INNER)
        .group_by(models.Restaurant.name)
        .order_by(SQL("avg_rating").desc())
    )

    for restaurant in query:
        print(restaurant.name, restaurant.avg_rating)

    best_rest = models.Restaurant.get(models.Restaurant.name == query[0].name)
    print(best_rest)
    return best_rest


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
    ...


def add_dish_to_menu() -> models.Dish:
    """You have created a new dish for your restaurant and want to add it to the menu

    The dish you create must at the very least contain 'cheese'.
    You do not know which ingredients are in the database, but you must not
    create ingredients that already exist in the database. You may create
    new ingredients however.
    Return your newly created dish
    """
    ...
