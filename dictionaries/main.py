__winc_id__ = "25a8041d2d5e4e3ab61ab1be43bfb863"
__human_name__ = "dictionaries"

from helpers import get_countries


def create_passport(name, date_of_birth, place_of_birth, height, nationality):

    passport = {
        "name": name,
        "date_of_birth": date_of_birth,
        "place_of_birth": place_of_birth,
        "height": height,
        "nationality": nationality,
    }

    return passport


# adds or updates a passport with a 'stamp' of the visited country
def add_stamp(passport, country):

    # only stamp if visited country is not the home country
    if country != passport["nationality"]:
        # if passport has no previous stamps
        # create a key-value pair for stamps: country
        if "stamps" not in passport:
            passport["stamps"] = [country]
        # only add stamp if country has not already been added to stamps
        if country not in passport["stamps"]:
            passport["stamps"].append(country)

    return passport


# Stamps a passport when a person is allowed to travel to a specific destination country.
# Checks if
# - traveling to the destination is allowed by it's own country of citizenship
# - the person has not visited a country that is forbidden by the destination country
def check_passport(passport, destination, allowed_destinations, forbidden_countries):
    nationality = passport["nationality"]

    # do not stamp passport if person visited - or is a citizen - of a forbidden country
    if destination in forbidden_countries:
        for country in forbidden_countries[destination]:
            if country in passport["stamps"] or country == nationality:
                return False

    # check if person is allowed to travel to destination country:
    if nationality in allowed_destinations:
        if destination in allowed_destinations[nationality]:
            add_stamp(passport, destination)
            return passport
    else:
        return False


# dict of countries that citizens that are from this country
# are allowed to travel to by that country.
allowed_destinations = {
    "Belgium": ["Netherlands", "Italy", "France"],
    "Netherlands": ["Belgium", "Germany"],
    "Australia": ["Netherlands"],
}

# dict of countries that a person is not allowed to have visited
# as forbidden by the destination country.
forbidden_countries = {
    "Netherlands": ["United Kingdom", "Egypt"],
    "Australia": ["New Zealand", "Singapore"],
}

if __name__ == "__main__":
    Janneke = create_passport("Janneke", "1995-08-01", "Utrecht", 1.73, "Netherlands")
    Tim = create_passport("Tim", "1956-01-02", "Melbourne", 1.83, "Australia")

    print(Janneke)
    print(add_stamp(Janneke, "Vietnam"))
    print(add_stamp(Janneke, "Italy"))
    print(add_stamp(Janneke, "Guam"))

    # print(check_passport(Janneke, "Belgium", allowed_destinations, forbidden_countries))
    # print(Tim)
    # print(add_stamp(Tim, "Belgium"))
    # print(check_passport(Tim, "Netherlands", allowed_destinations, forbidden_countries))
