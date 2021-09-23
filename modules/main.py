# Do not modify these lines
__winc_id__ = "78029e0e504a49e5b16482a7a23af58c"
__human_name__ = "modules"

# Add your code after this line

import this
import time
import math
import datetime
import sys
import greet


# Write a function 'wait' that takes one argument,
# using a function in the time module to make the computer wait for a number of seconds,
# then returns nothing.
def wait(seconds):

    print("Executing wait function")
    print(f"Waiting {seconds} seconds")
    time.sleep(seconds)


# Implement a function my_sin that takes one argument (float)
# and returns the sine of that float.
def my_sin(a):

    return math.sin(a)


# Implement a function that returns a string with the current date + time
# up to the minute in the ISO 8601 format.
def iso_now():

    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%dT%H:%M")


# Implement a function that returns a string
# which shows which platform you are on
def platform():

    return sys.platform


# Create a new file greet.py and implement a function 'supergreeting'
# that personalises a string of the form 'Hellooo...ooo, Bob!' with a name.
# Then import this function in main.py and write a function supergreeting_wrapper
# that calls supergreeting with it and returns the result.
def supergreeting_wrapper(name):

    return greet.supergreeting(name)


if __name__ == "__main__":
    print(wait(2))
    print(my_sin(1.5))
    print(iso_now())
    print(platform())
    print(supergreeting_wrapper("Bob"))
