from random import randint


class Dice(object):

    def __init__(self):
        self.value = 1
        self.points = 1

    def json(self):
        return {
            "value": self.value,
            "points": self.points,
        }

    def throw(self):
        self.value = randint(1, 6)
        self.points = 5 if self.value == 6 else self.value
