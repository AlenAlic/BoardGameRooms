from datetime import datetime


class Player(object):

    def __init__(self, player_id=None, name=None):
        self.player_id = player_id
        self.name = name
        self.active = True
        self.dice = []
        self.tiles = []

    def json(self):
        return {
            "player_id": self.player_id,
            "name": self.name,
            "dice": [dice.json() for dice in self.dice],
            "tiles": [tile.json() for tile in self.tiles],
            "active": self.active,
            "score": self.score,
        }

    @property
    def score(self):
        return sum([tile.worms for tile in self.tiles])

    @property
    def highest_tile(self):
        tile_values = [tile.value for tile in self.tiles]
        return max(tile_values) if tile_values else 0

    def take_dice(self, value):
        taken_dice = [dice for dice in self.dice if dice.value == value]
        kept_dice = [dice for dice in self.dice if dice.value != value]
        self.dice = kept_dice
        return taken_dice

    def give_dice(self, dice):
        self.dice.extend(dice)

    def take_tile(self, value):
        taken_tile = [tile for tile in self.tiles if tile.value == value]
        kept_tiles = [tile for tile in self.tiles if tile.value != value]
        self.tiles = kept_tiles
        return taken_tile[0]

    def give_tile(self, tile):
        tile.order = datetime.utcnow().timestamp()
        self.tiles.append(tile)

    def sort_tiles(self):
        self.tiles.sort(key=lambda tile: tile.value)
