__winc_id__ = "9920545368b24a06babf1b57cee44171"
__human_name__ = "refactoring"


class Homeowner:
    def __init__(self, name, address, needs):
        self.name = name
        self.address = address
        self.needs = needs


class Specialist:
    def __init__(self, name, rate):
        self.name = name
        self.rate = rate


class Electrician(Specialist):
    profession = "electrician"


class Painter(Specialist):
    profession = "painter"


class Plumber(Specialist):
    profession = "plumber"


all_electricians = []
all_painters = []
all_plumbers = []


def add_specialist(specialists):
    for specialist in specialists:
        if specialist.profession == "electrician":
            all_electricians.append(specialist)
        if specialist.profession == "painter":
            all_painters.append(specialist)
        if specialist.profession == "plumber":
            all_plumbers.append(specialist)


def cheapest(profession):
    if profession == "electrician":
        return min(all_electricians, key=lambda electrician: electrician.rate).name
    if profession == "plumber":
        return min(all_plumbers, key=lambda plumber: plumber.rate).name
    if profession == "painter":
        return min(all_painters, key=lambda painter: painter.rate).name


def show_contracts(homeowner):
    contracts = []
    for need in homeowner.needs:
        if need == "electrician":
            contracts.append(cheapest("electrician"))
        elif need == "painter":
            contracts.append(cheapest("painter"))
        elif need == "plumber":
            contracts.append(cheapest("plumber"))
    return contracts


alice = Electrician("Alice Aliceville", 150)
andrea = Electrician("Andrea Andreaville", 135)
bob = Painter("Bob Bobsville", 145)
berry = Painter("Berry Berryville", 169)
craig = Plumber("Craig Craigsville", 195)
corry = Plumber("Corry Corryville", 115)

alfred = Homeowner("Alfred Alfredson", "Alfredslane 123", ["painter", "plumber"])
bert = Homeowner("Bert Bertson", "Bertslane 231", ["plumber"])
candy = Homeowner("Candy Candison", "Candylane 312", ["electrician", "painter"])

add_specialist([alice, andrea, bob, berry, craig, corry])
print(cheapest("painter"))
print(show_contracts(alfred))


# create list of instances outside of class instead of
# making it a class variable and using it in a class method:
# better to separate logic of application (vinden van cheapest specialist)
# met het moduleren van werkelijkheid dmv class structuur
# alles wat in de class zit zou te maken moeten hebben met moduleren van de instance zelf,
# en niet een probleem porberen op te lossen dat gerelateerd is aan die instances
# omdat het probleem vaak evolved over time.
# bv als je lijst binnen de class stopt, moet je class aanpassen als probleem veranderd
# bijv. vinden van max ipv van min rate
# dit zou voor issues zorgen als je samenwerkt and andere gebruikendezelfde lijst
