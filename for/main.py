from helpers import get_countries


""" Leave this untouched. Wincpy uses it to match this assignment with the
tests it runs. """
__winc_id__ = "c545bc87620d4ced81cbddb8a90b4a51"
__human_name__ = "for"


""" Write your functions here. """
# returns a list of country names that have the shortest length


def shortest_names(countries):
    shortest_name_lenght = 100
    shortest_names = []

    # loop through countries and define the lenght of the shortest names
    for country in countries:
        name_lenght = len(country)
        if name_lenght < shortest_name_lenght:
            shortest_name_lenght = name_lenght

    # if country name equals shortest lenght than add to list
    for country in countries:
        if len(country) == shortest_name_lenght:
            shortest_names.append(country)

    return shortest_names


# returns a list with the top 3 countries that have the most vowels in their name
def most_vowels(countries):
    vowels = "aeiouAEIOU"

    top_1_count = 0
    top_2_count = 0
    top_3_count = 0

    top_1 = 0
    top_2 = 0
    top_3 = 0

    for country in countries:
        # find the vowel_count per country
        vowel_count = 0
        for letter in country:
            if letter in vowels:
                vowel_count = vowel_count + 1
        # check if vowel_count belongs in top 3
        # degrade countries 1 step
        if vowel_count >= top_1_count:
            top_3_count = top_2_count
            top_2_count = top_1_count
            top_1_count = vowel_count
            top_3 = top_2
            top_2 = top_1
            top_1 = country
        elif vowel_count >= top_2_count:
            top_3_count = top_2_count
            top_2_count = vowel_count
            top_3 = top_2
            top_2 = country
        elif vowel_count >= top_3_count:
            top_3_count = vowel_count
            top_3 = country
    return [top_1, top_2, top_3]


# returns a list of country names whose letters can be combined to form the complete alphabet
def alphabet_set(countries):
    alphabet = list("abcdefghijklmnopqrstuvwxyz")
    alphabet_countries = []

    for country in countries:
        removed_letters = False
        # for each letter in a countries name,
        # check if its in the alphabet
        # and remove the letter from the alphabet
        for letter in country:
            if letter.lower() in alphabet:
                alphabet.remove(letter.lower())
                removed_letters = True
        # If a country removed letters from the alphabet
        # add the country to the list
        if removed_letters:
            alphabet_countries.append(country)

    return alphabet_countries


# This block is only run if this file is the entrypoint; python main.py
# It is not run if it is imported as a module: `from main import *`
if __name__ == "__main__":
    countries = get_countries()

    """ Write the calls to your functions here. """
    print(shortest_names(countries))
    print(most_vowels(countries))
    print(list("abcdefghijklmnopqrstuvwxyz"))
    print(alphabet_set(countries))
