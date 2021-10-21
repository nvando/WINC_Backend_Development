# Do not modify these lines
__winc_id__ = "04da020dedb24d42adf41382a231b1ed"
__human_name__ = "classes"

# Add your code after this line
class Player:
    def __init__(self, name, speed, endurance, accuracy):
        self.name = name
        if 0 < speed < 1:
            self.speed = speed
        if 0 < endurance < 1:
            self.endurance = endurance
        if 0 < accuracy < 1:
            self.accuracy = accuracy
        else:
            raise ValueError

    def introduce(self):
        return f"Hello everyone, my name is {self.name}."

    def strength(self):
        # returns a tuple with the player's highest attribute
        # and the corresponding attribute value.
        # If multiple attributes share the same value,
        # prioritize by speed > endurance > accuracy.
        if self.speed >= self.endurance and self.speed >= self.accuracy:
            return ("speed", self.speed)
        elif self.endurance > self.speed and self.endurance >= self.accuracy:
            return ("endurance", self.endurance)
        else:
            return ("accuracy", self.accuracy)


class Commentator:
    def __init__(self, name):
        self.name = name

    def sum_player(self, player):
        return player.speed + player.endurance + player.accuracy

    def compare_players(self, player1, player2, attribute):
        # returns the name of the player that scores the highest
        # on the attribute argument. If the players score equally,
        # return the player that has the highest strength.
        # If these are also equal, reports the player
        # who has the highest total score according to sum_player.
        attribute_player1 = getattr(player1, attribute)
        attribute_player2 = getattr(player2, attribute)
        if attribute_player1 > attribute_player2:
            return player1.name
        elif attribute_player1 < attribute_player2:
            return player2.name
        else:
            strength_player1 = player1.strength()[1]
            strength_player2 = player2.strength()[1]
            if strength_player1 > strength_player2:
                return player1.name
            if strength_player1 < strength_player2:
                return player2.name
            else:
                sum_player1 = self.sum_player(player1)
                sum_player2 = self.sum_player(player2)
                if sum_player1 > sum_player2:
                    return player1.name
                if sum_player1 < sum_player2:
                    return player2.name
                else:
                    return "These two players might as well be twins!"


if __name__ == "__main__":
    player1 = Player("Bob", 0.1, 0.6, 0.9)
    player2 = Player("Rita", 0.1, 0.5, 0.8)
    print(player2.introduce())
    print(player2.strength())
    ray = Commentator("Ray Hudson")
    print(ray.sum_player(player2))
    print(ray.compare_players(player1, player2, "accuracy"))
