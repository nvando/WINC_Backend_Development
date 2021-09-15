# Do not modify these lines
__winc_id__ = "6eb355e1a60f48a28a0bbbd0c88d9ab4"
__human_name__ = "lists"

# Add your code after this line


def alphabetical_order(movies):
    return sorted(movies)


def won_golden_globe(movie):
    winners = [
        "jaws",
        "star wars: episode iv – a new hope",
        "e.t. the extra-terrestrial",
        "memoirs of a geisha",
    ]
    if movie.lower() in winners:
        return True
    else:
        return False


def remove_toto_albums(movies):
    if "Fahrenheit" in movies:
        movies.remove("Fahrenheit")
    if "The Seventh One" in movies:
        movies.remove("The Seventh One")
    if "Toto XX" in movies:
        movies.remove("Toto XX")
    if "Falling in Between" in movies:
        movies.remove("Falling in Between")
    if "35th Anniversary – Live in Poland" in movies:
        movies.remove("35th Anniversary – Live in Poland")
    if "Toto XIV" in movies:
        movies.remove("Toto XIV")
    if "Old Is New" in movies:
        movies.remove("Old Is New")
    if "40 Tours Around the Sun" in movies:
        movies.remove("40 Tours Around the Sun")
    if "With a Little Help from My Friends" in movies:
        movies.remove("With a Little Help from My Friends")
    return movies


movies = [
    "Superman",
    "Fahrenheit",
    "Schindler's list",
    "Seven years in Tibet",
    "Toto XX",
    "Juresic Park",
]
print(alphabetical_order(movies))
print(won_golden_globe("Memoirs of a Geisha"))
print(remove_toto_albums(movies))
