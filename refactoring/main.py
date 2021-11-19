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
                self.contracts.append(Electrician.cheapest())
            elif need == "painter":
                print("needs painter")
                self.contracts.append(Painter.cheapest())
            elif need == "plumber":
                self.contracts.append(Plumber.cheapest())
        return self.contracts


class Specialist:
    def __init__(self, name, rate):
        self.name = name
        self.rate = rate


class Electrician(Specialist):
    profession = "electrician"
    all_electricians = []

    def __init__(self, name, rate):
        super().__init__(name, rate)
        Electrician.all_electricians.append(self)
        print(f"added {self.name} to list")

    @classmethod
    def cheapest(cls):
        return min(cls.all_electricians, key=lambda electrician: electrician.rate).name


class Painter(Specialist):
    profession = "painter"
    all_painters = []

    def __init__(self, name, rate):
        super().__init__(name, rate)
        Painter.all_painters.append(self)
        print(f"added {self.name} to list")

    @classmethod
    def cheapest(cls):
        return min(cls.all_painters, key=lambda painter: painter.rate).name


class Plumber(Specialist):
    profession = "plumber"
    all_plumbers = []

    def __init__(self, name, rate):
        super().__init__(name, rate)
        Plumber.all_plumbers.append(self)
        print(f"added {self.name} to list")

    @classmethod
    def cheapest(cls):
        return min(cls.all_plumbers, key=lambda plumber: plumber.rate).name


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
print(f"The cheapest electrician is {Electrician.cheapest()}")
print(alfred.contracts())
print


# professionals
# alice_name = 'Alice Aliceville'
# alice_profession = 'electrician'
# bob_name = 'Bob Bobsville'
# bob_profession = 'painter'
# craig_name = 'Craig Craigsville'
# craig_profession = 'plumber'

# homeowners
# alfred_name = 'Alfred Alfredson'
# alfred_address = 'Alfredslane 123'
# alfred_needs = ['painter', 'plumber']
# bert_name = 'Bert Bertson'
# bert_address = 'Bertslane 231'
# bert_needs = ['plumber']
# candice_name = 'Candice Candicedottir'
# candice_address = 'Candicelane 312'
# candice_needs = ['electrician', 'painter']

# alfred_contracts = []
# for need in alfred_needs:
#     if need == alice_profession:
#         alfred_contracts.append(alice_name)
#     elif need == bob_profession:
#         alfred_contracts.append(bob_name)
#     elif need == craig_profession:
#         alfred_contracts.append(craig_name)

# bert_contracts = []
# for need in bert_needs:
#     if need == alice_profession:
#         bert_contracts.append(alice_name)
#     elif need == bob_profession:
#         bert_contracts.append(bob_name)
#     elif need == craig_profession:
#         bert_contracts.append(craig_name)

# candice_contracts = []
# for need in candice_needs:
#     if need == alice_profession:
#         candice_contracts.append(alice_name)
#     elif need == bob_profession:
#         candice_contracts.append(bob_name)
#     elif need == craig_profession:
#         candice_contracts.append(craig_name)

# print("Alfred's contracts:", alfred_contracts)
# print("Bert's contracts:", bert_contracts)
# print("Candice's contracts:", candice_contracts)
