from helpers import random_koala_fact

__winc_id__ = "c0dc6e00dfac46aab88296601c32669f"
__human_name__ = "while"


# returns the requested number of unique koala facts in a list
def unique_koala_facts(num_unique_facts):
    unique_facts = []
    facts_added = 0

    # keep requesting facts until 1000 request have been made
    requested_facts = 0
    while requested_facts < 1000:
        requested_facts += 1
        new_fact = random_koala_fact()

        # check wheather fact is unique
        # and add fact to list
        # and count unique facts
        if new_fact not in unique_facts:
            unique_facts.append(new_fact)
            facts_added += 1

        # stop requesting facts when number of added facts equeals input number
        if facts_added == num_unique_facts:
            break

    return unique_facts


# shows the number of unique facts mentioning joey's in the facts dataset
# by requesting facts until one particular fact is seen 10 times
def num_joey_facts():
    flag_fact = random_koala_fact()
    flag_counter = 0
    joey_facts = []
    num_joey_facts = 0

    # request facts from database
    while flag_counter < 10:
        new_fact = random_koala_fact()
        # if the fact equals the flag fact, add to counter
        if new_fact == flag_fact:
            flag_counter += 1
        # check if fact mentions 'joey'
        if "joey" in new_fact.lower():
            # check if fact has not already been counted
            if new_fact not in joey_facts:
                # count fact and add fact to list
                num_joey_facts += 1
                joey_facts.append(new_fact)

    return num_joey_facts


# return the weight of koala, by checking the facts in the dataset
def koala_weight():

    while True:
        new_fact = random_koala_fact()
        if "kg" in new_fact:
            first_part = new_fact.split("kg")[0]
            last_space_index = first_part.rindex(" ")
            weight = int(first_part[last_space_index + 1 :])
            break
    return weight


# This block is only executed if this script is run directly (python main.py)
# It is not run if you import this file as a module.
if __name__ == "__main__":
    # print(random_koala_fact())
    print(unique_koala_facts(5))
    print(num_joey_facts())
    print(koala_weight())
