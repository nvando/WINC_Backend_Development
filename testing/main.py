def get_none():
    print("returning None")


def flatten_dict(d):
    return list(d.values())


def flatten_nested_dict(d, flattened_d=None):
    # Using None instead of the mutable [] object because:
    # Default arguments are evaluated in Pyhton once when the function is defined,
    # not each time the function is called,
    # and the arguments become attributes of the function object.
    # If we use [] and mutatate it during the call,
    # that object stays mutated for all future calls to the function as well.
    if flattened_d is None:
        flattened_d = {}

    for k, v in d.items():

        if not isinstance(v, dict):
            print("not nested:", k, v)
            flattened_d[k] = v
        else:
            print("nested:", k, v)
            print("flatten dict en add values:")
            flatten_nested_dict(v, flattened_d)

    print(flattened_d.values())
    return list(flattened_d.values())


if __name__ == "__main__":
    d = {"Tim": {"suburb": "collaroy", "age": 21}, "Lana": "No Info"}
    d2 = {"a": {"inner_a": 41, "inner_b": 350}, "b": 3.14}
    print(flatten_nested_dict(d))
    print(flatten_nested_dict(d2))
