import peewee

db = peewee.SqliteDatabase("YumYum.db")


class Ingredient(peewee.Model):
    name = peewee.CharField()
    is_vegetarian = peewee.BooleanField()
    is_vegan = peewee.BooleanField()
    is_glutenfree = peewee.BooleanField()

    class Meta:
        database = db


class Restaurant(peewee.Model):
    name = peewee.CharField()
    open_since = peewee.DateField()
    opening_time = peewee.TimeField()
    closing_time = peewee.TimeField()

    class Meta:
        database = db


class Dish(peewee.Model):
    name = peewee.CharField()
    served_at = peewee.ForeignKeyField(Restaurant)
    price_in_cents = peewee.IntegerField()
    ingredients = peewee.ManyToManyField(Ingredient)

    class Meta:
        database = db


class Rating(peewee.Model):
    restaurant = peewee.ForeignKeyField(Restaurant)
    rating = peewee.IntegerField()
    comment = peewee.CharField(null=True)

    class Meta:
        database = db


DishIngredient = Dish.ingredients.get_through_model()


def populate_test_data():
    db.create_tables([Ingredient, Restaurant, Dish, Rating, DishIngredient])

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

    for name, diet in ingredients_data:
        Ingredient.create(name=name, is_vegan=diet[0], is_vegetarian=diet[1], is_glutenfree=diet[2])

    dishes_data = (
        ("pasta carbonara", "Pinokio", 1500),
        ("pasta napolitana", "Casa di Pasta", 1300),
        ("pasta pollo", "Florencia", 1400),
        ("pizza margarita", "Pinokio", 1100),
        ("risotto vegatariana", "Florencia", 1000),
    )

    for dish in dishes_data:
        Dish.create(name=dish[0], served_at=dish[1], price_in_cents=dish[2])

    dish_ingredients = (
        ("pasta carbonara", ("pasta", "pork", "cheese")),
        ("pasta napolitana", ("pasta", "tomato", "pinenut")),
        ("pasta pollo", ("pasta", "chicken", "tomato")),
        ("pizza margarita", ("flour", "tomato", "cheese")),
        ("risotto vegatariana", ("risotto", "tomato", "potato", "pinenut")),
    )

    for dish_name, ingredients in dish_ingredients:
        dish = Dish.get(Dish.name == dish_name)
        print(dish.name)
        for ingredient in ingredients:

            ing = Ingredient.get(Ingredient.name == ingredient)
            dish.ingredients = ing
            dish.save
            print(dish.name, ing.is_vegan)

        #  Dish.ingredients.add(ing)
        # dish.save()

    # favorite_data = (
    #     ('huey', ['whine']),
    #     ('mickey', ['purr']),
    #     ('zaizee', ['meow', 'purr']))
    # for username, favorites in favorite_data:
    #     user = User.get(User.username == username)
    #     for content in favorites:
    #         tweet = Tweet.get(Tweet.content == content)
    #         Favorite.create(user=user, tweet=tweet)
