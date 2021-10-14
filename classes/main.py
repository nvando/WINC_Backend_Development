# Do not modify these lines
__winc_id__ = "04da020dedb24d42adf41382a231b1ed"
__human_name__ = "classes"

# Add your code after this line
class Player:
    def __init__(self, name, speed, endurance, accuracy):
        self.name = name
        # self.speed = speed
        self.endurance = endurance
        self.accuracy = accuracy
        # if (speed or endurance or accuracy) > 1:
        #     raise ValueError
        if 0 < speed < 1:
            self.speed = speed
        else:
            raise ValueError

    def introduce(self):
        return f"Hello everyone, my name is {self.name}."

    def strength(self):
        if self.speed >= self.endurance and self.speed >= self.accuracy:
            highest_name = "speed"
            highest_value = self.speed
        elif self.endurance > self.speed and self.endurance >= self.accuracy:
            highest_name = "endurance"
            highest_value = self.endurance
        elif self.accuracy > self.speed and self.accuracy > self.endurance:
            highest_name = "accuracy"
            highest_value = self.accuracy
        return (highest_name, highest_value)


class Commentator:
    def __init__(self, name):
        self.name = name

    def sum_player(self, player):
        return player.speed + player.endurance + player.accuracy

    def compare_players(self, player1, player2, attribute):
        pass


if __name__ == "__main__":
    player1 = Player("Bob", 0.2, 0.5, 0.8)
    Player2 = Player("Rita", 0.1, 0.9, 0.7)
    print(Player2.introduce())
    print(Player2.strength())
    ray = Commentator("Ray Hudson")
    print(ray.sum_player(Player2))
