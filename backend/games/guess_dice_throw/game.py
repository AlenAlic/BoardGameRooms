from backend.models.game import Game
from random import randint


class GuessDiceThrow(Game):

    def __init__(self):
        super().__init__()
        self.guesses = {}
        self.throw = 0

    @property
    def tag(self):
        return "GDT"

    @property
    def name(self):
        return "Guess Dice Throw"

    @property
    def min_players(self):
        return 1

    @property
    def max_players(self):
        return 10

    @property
    def rejoinable(self):
        return True

    @property
    def game_json(self):
        return {
            "guesses": self.guesses,
            "throw": self.throw
        }

    @property
    def actions(self):
        return {
            "GUESS": self.set_guess,
            "THROW_DICE": self.throw_dice,
            "NEW_GAME": self.new_game
        }

    def set_guess(self, data):
        self.guesses[data["user_id"]] = data["guess"]

    def throw_dice(self):
        self.throw = randint(1, 6)

    def new_game(self):
        self.guesses = {}
        self.throw = 0
