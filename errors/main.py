# Do not modify these lines
import os

__winc_id__ = "534d85ea1ab14924a91f9eccf6f3f30d"
__human_name__ = "errors"


# Test your functions here to make sure the functionality remains the same.
def main():
    print(add(5, "ten"))
    print(read_file(r"Back-end Assignments\files\cache\600.txt"))
    foo = list(range(10))
    print(foo)
    print(
        get_item_from_list(foo, 9),
        get_item_from_list(foo, -1),
        get_item_from_list(foo, 10),
    )
    ...


"""Change the three functions below from Look Before You Leap (LBYL) to Easier
to Ask for Forgiveness than Permission (EAFP)"""


# Returns the addition of x and y if it's defined, otherwise returns 0
def add(x, y):
    try:
        return x + y
    except TypeError:
        return 0


# Returns the contents of the file at 'filename', or an empty string if the
# file does not exist
def read_file(filename):
    try:
        return open(filename, "r").read()
    except FileNotFoundError:
        print("File not found")
        return ""


# Returns item at `index` from list `l` if possible, otherwise returns None
def get_item_from_list(l, index):
    try:
        return l[index]
    except IndexError:
        print("List index out of range")


if __name__ == "__main__":
    main()
