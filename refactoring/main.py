__winc_id__ = "9920545368b24a06babf1b57cee44171"
__human_name__ = "refactoring"


class Homeowner:
    def __init__(self, name, address, needs):
        self.name = name
        self.address = address
        self.needs = needs

    def contracts(self):
        self.contracts = []
        for need in self.needs:
            if need == "electrician":
                self.contracts.append(Electrician.find_cheapest())
            elif need == "painter":
                print("needs painter")
                self.contracts.append(Painter.find_cheapest())
            elif need == "plumber":
                self.contracts.append(Plumber.find_cheapest())
        return self.contracts


class Specialist:
    all_specialists = []

    def __init__(self, name, rate):
        self.name = name
        self.rate = rate
        self.all_specialists.append(self)
        print(f"added {self.name} to list")

    @classmethod
    def find_cheapest(cls):
        specialists_filtered = [
            specialist
            for specialist in cls.all_specialists
            if cls.__name__ == specialist.__class__.__name__
        ]
        return min(specialists_filtered, key=lambda specialist: specialist.rate).name


class Electrician(Specialist):
    profession = "electrician"
    all_specialists = []

    def __init__(self, name, rate):
        super().__init__(name, rate)


class Painter(Specialist):
    profession = "painter"

    def __init__(self, name, rate):
        super().__init__(name, rate)


class Plumber(Specialist):
    profession = "plumber"

    def __init__(self, name, rate):
        super().__init__(name, rate)


alice = Electrician("Alice Aliceville", 150)
andrea = Electrician("Andrea Andreaville", 135)
bob = Painter("Bob Bobsville", 145)
berry = Painter("Berry Berryville", 169)
craig = Plumber("Craig Craigsville", 195)
corry = Plumber("Corry Corryville", 115)

alfred = Homeowner("Alfred Alfredson", "Alfredslane 123", ["painter", "plumber"])
bert = Homeowner("Bert Bertson", "Bertslane 231", ["plumber"])
candy = Homeowner("Candy Candison", "Candylane 312", ["electrician", "painter"])

print(f"alfred's full name is {alfred.name}")
print(f"The cheapest electrician is {Electrician.find_cheapest()}")
print(alfred.contracts())
print(Electrician.find_cheapest())
print(Painter.find_cheapest())
print(Plumber.find_cheapest())
