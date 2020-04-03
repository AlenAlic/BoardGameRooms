from .guess_dice_throw import GuessDiceThrow

GAMES_LIST = [GuessDiceThrow]


def get_game(tag):
    games = {game.tag: game for game in [g() for g in GAMES_LIST]}
    games[None] = None
    return games[tag]
