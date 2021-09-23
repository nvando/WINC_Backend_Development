# Do not modify these lines
__winc_id__ = "7b9401ad7f544be2a23321292dd61cb6"
__human_name__ = "arguments"


# return a personalised greeting
def greet(name, greeting="Hello, <name>!"):

    return greeting.replace("<name>", name)


# returns the force exerted given a specific mass and (celestial) body
def force(mass, body="earth"):

    gravity = {
        "sun": 274.0,
        "jupiter": 24.9,
        "neptune": 11.2,
        "saturn": 10.4,
        "earth": 9.8,
        "uranus": 8.9,
        "venus": 8.9,
        "mars": 3.7,
        "mercury": 3.7,
        "moon": 1.6,
        "pluto": 0.6,
    }

    force = mass * gravity[body]
    return force


# returns the gravitional pull that object m1 and m2
# have on each other when d meters apart
def pull(m1, m2, d):

    pull = (6.674 * 10 ** -11) * ((m1 * m2) / d ** 2)
    return pull


if __name__ == "__main__":
    print(greet("Bob"))
    print(force(2))
    print(pull(1, 2, 10))
