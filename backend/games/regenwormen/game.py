from backend.models.game import Game
from .player import Player
from .tile import Tile
from .dice import Dice
from random import shuffle


BOARD = "board"
TILES = {
    21: 1, 22: 1, 23: 1, 24: 1, 25: 2, 26: 2, 27: 2, 28: 2, 29: 3, 30: 3, 31: 3, 32: 3, 33: 4, 34: 4, 35: 4, 36: 4
}


class Regenwormen(Game):

    def __init__(self):
        super().__init__()
        board = Player(BOARD)
        board.tiles = [Tile(value, worms) for value, worms in TILES.items()]
        board.dice = self.new_dice()
        self.board = board
        self.players = {board.player_id: board}
        self.current_player = None
        self.order = []
        self.dice_thrown = False
        self.started = False
        self.turn_over = False

    @property
    def tag(self):
        return "RWM"

    @property
    def name(self):
        return "Regenwormen"

    @property
    def min_players(self):
        return 2

    @property
    def max_players(self):
        return 7

    @property
    def rejoinable(self):
        return True

    @property
    def game_json(self):
        return {
            "board": self.board.json(),
            "players": {player_id: player.json() for player_id, player in self.players.items()},
            "current_player": self.current_player,
            "order": self.order,
            "dice_thrown": self.dice_thrown,
            "started": self.started,
            "turn_over": self.turn_over,
            "winner": self.winner,
            "scores": self.scores,
        }

    @property
    def winner(self):
        players = [player for player in self.players.values() if player.player_id != BOARD]
        if len(players) == 0:
            return None
        scores = [player.score for player in players]
        max_score = max(scores) if scores else 0
        players = [player for player in players if player.score == max_score]
        if len(players) == 1:
            return players[0].player_id
        else:
            values = [player.highest_tile for player in players]
            max_value = max(values) if values else 0
            return [player for player in players if player.highest_tile == max_value][0].player_id

    @property
    def scores(self):
        players = sorted([p for p in self.players.values() if p.player_id != BOARD],
                         key=lambda x: x.score, reverse=True)
        return {p.player_id: p.score for p in players}

    @property
    def actions(self):
        return {
            "START": self.start_game,
            "THROW_DICE": self.throw_dice,
            "CHOOSE_DICE": self.choose_dice,
            "TAKE_TILE": self.take_tile,
            "END_TURN": self.end_turn,
        }

    def deactivate_user(self, user_id):
        super().deactivate_user(user_id)
        self.players[user_id].active = False
        if user_id == self.current_player:
            self.end_turn()

    def rejoin(self, user):
        super().rejoin(user)
        self.players[user.user_id].active = False

    @staticmethod
    def new_dice():
        return [Dice() for _ in range(8)]

    def set_next_player(self):
        next_index = (self.order.index(self.current_player) + 1) % len(self.order)
        next_player_id = self.order[next_index]
        for _ in range(len(self.order)):
            if self.players[next_player_id].active:
                self.current_player = self.order[next_index]
                break
            else:
                next_index += 1

    def start_game(self, data):
        for user in data["players"]:
            self.players[user["user_id"]] = Player(player_id=user["user_id"], name=user["username"])
        self.order = [user_id for user_id in self.players.keys() if user_id != BOARD]
        shuffle(self.order)
        self.current_player = self.order[0]
        self.started = True

    def throw_dice(self):
        for dice in self.board.dice:
            dice.throw()
        self.dice_thrown = True
        board_values = set([dice.value for dice in self.board.dice])
        player_values = set([dice.value for dice in self.players[self.current_player].dice])
        self.turn_over = board_values.issubset(player_values)

    def choose_dice(self, data):
        player_id = data["user_id"]
        value = data["value"]
        self.players[player_id].give_dice(self.board.take_dice(value))
        self.dice_thrown = False
        self.turn_over = \
            len(self.board.dice) == 0 and 6 not in [dice.value for dice in self.players[self.current_player].dice]

    def take_tile(self, data):
        user_id = data["user_id"]
        player_id = data["player_id"]
        value = data["value"]
        self.players[user_id].give_tile(self.players[player_id].take_tile(value))
        self.end_turn()

    def remove_last_tile(self):
        tiles = self.players[self.current_player].tiles
        if len(tiles) > 0:
            value = tiles[-1].value
            self.board.give_tile(self.players[self.current_player].take_tile(value))
            self.board.sort_tiles()
            active_tiles = [tile for tile in self.board.tiles if tile.active]
            if len(active_tiles) > 0:
                last_tile = active_tiles[-1]
                if last_tile.value < value:
                    last_tile.active = False

    def end_turn(self):
        if self.turn_over:
            self.remove_last_tile()
        for player in self.players.values():
            player.dice = []
        self.board.dice = self.new_dice()
        self.set_next_player()
        self.dice_thrown = False
        self.turn_over = False
