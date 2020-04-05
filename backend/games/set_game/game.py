from backend.models.game import Game
from .card import Card, COLORS, NUMBERS, FILLS, SHAPES
from random import shuffle
from itertools import combinations
from backend.socket.games.functions import send_game_message


class Set(Game):

    def __init__(self):
        super().__init__()
        cards = []
        for color in COLORS:
            for number in NUMBERS:
                for fill in FILLS:
                    for shape in SHAPES:
                        cards.append(Card(color, number, fill, shape))
        shuffle(cards)
        self.cards = cards[:12]
        self.remaining_cards = []
        self.scores = {}
        self.sets = {}
        self.started = False
        self.active = False
        self.current_player = None
        self.selected_cards = []
        self.game_over = False
        self.error_cards = []

    @property
    def tag(self):
        return "SET"

    @property
    def name(self):
        return "Set"

    @property
    def min_players(self):
        return 1

    @property
    def max_players(self):
        return 8

    @property
    def rejoinable(self):
        return True

    @property
    def game_json(self):
        return {
            "cards": [c.json() for c in self.cards],
            "remaining_cards": len(self.remaining_cards),
            "scores": self.scores,
            "sets": self.sets,
            "started": self.started,
            "active": self.active,
            "current_player": self.current_player,
            "selected_cards": self.selected_cards,
            "game_over": self.game_over,
            "winners": self.winners,
            "error_cards": self.error_cards,
        }

    @property
    def actions(self):
        return {
            "START_GAME": self.start_game,
            "CALL_SET": self.call_set,
            "SELECT_CARD": self.select_card,
            "CHECK_SET": self.check_set,
            "CHECK_BOARD": self.check_board,
            "NO_CHOICE": self.no_choice
        }

    @property
    def winners(self):
        high_score = max([v for v in self.scores.values()]) if len(self.scores.values()) > 0 else 0
        return [user_id for user_id, score in self.scores.items() if score == high_score]

    def start_game(self):
        self.scores = {user_id: 0 for user_id in self.users}
        self.sets = {user_id: 0 for user_id in self.users}
        self.started = True
        self.active = True

    def call_set(self, data):
        if self.active:
            self.active = False
            self.current_player = data["user_id"]

    def select_card(self, data):
        tag = data["tag"]
        if tag in self.selected_cards:
            self.selected_cards = list(set([t for t in self.selected_cards if t != tag]))
        else:
            self.selected_cards.append(tag)
            self.selected_cards = list(set(self.selected_cards))
        # if len(self.selected_cards) == 3:
        #     self.check_set()

    def set_next_cards(self, cards):
        enough_remaining = len(self.remaining_cards) >= 3
        if len(self.cards) == 12:
            next_cards = self.remaining_cards[:3] if enough_remaining else [Card(placeholder=True)]*3
            for idx, card in enumerate(cards):
                pos = self.cards.index(card)
                self.cards[pos] = next_cards[idx]
        else:
            for card in cards:
                self.cards.remove(card)
        if enough_remaining:
            self.remaining_cards = self.remaining_cards[3:]

    def check_set(self):
        cards = [c for c in self.cards if c.tag in self.selected_cards]
        if self.compare_cards(cards):
            self.scores[self.current_player] += 1
            self.sets[self.current_player] += 1
            self.set_next_cards(cards)
        else:
            self.scores[self.current_player] -= 1
            self.error_cards = [c.tag for c in cards]
            send_game_message(self.room, "set_shake", [c.tag for c in cards])
        self.selected_cards = []
        self.current_player = None
        self.active = True

    @staticmethod
    def compare_cards(cards):
        colors = set([c.color for c in cards])
        numbers = set([c.number for c in cards])
        fills = set([c.fill for c in cards])
        shapes = set([c.shape for c in cards])
        return all([len(colors) == 3 or len(colors) == 1, len(numbers) == 3 or len(numbers) == 1,
                    len(fills) == 3 or len(fills) == 1, len(shapes) == 3 or len(shapes) == 1])

    def check_board(self):
        if self.check_board_cards():
            send_game_message(self.room, "board_size_same")
        else:
            if len(self.remaining_cards) >= 3:
                self.cards.extend(self.remaining_cards[:3])
                self.remaining_cards = self.remaining_cards[3:]
                send_game_message(self.room, "board_size_expanded")
            else:
                self.game_over = True

    def check_board_cards(self):
        combs = list(combinations([c for c in self.cards if not c.placeholder], 3))
        return any([self.compare_cards(comb) for comb in combs])

    def no_choice(self, data):
        if not self.active and data["user_id"] == self.current_player:
            self.scores[self.current_player] -= 1
            self.selected_cards = []
            self.current_player = None
            self.active = True
