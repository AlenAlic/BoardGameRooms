from inspect import getfullargspec


class Game(object):

    def __init__(self):
        self.users = {}
        self.active_users = []
        self.room = None

    @property
    def tag(self):
        """"
        Unique identifiers for the game
        """
        return ""

    @property
    def name(self):
        """"
        Name of the game, shown in the game lobby
        """
        return "Demo Game"

    @property
    def min_players(self):
        return 2

    @property
    def max_players(self):
        return 4

    @property
    def rejoinable(self):
        return False

    @property
    def game_json(self):
        """"
        JSON object specific to the game
        """
        return {}

    @property
    def actions(self):
        """"
        Dictionary of actions that the game can do.
        Each actions maps to a function
        """
        return {
            "PRINT": self.demo_action_data,
            "PASS": self.demo_action,
        }

    def json(self):
        """"
        JSON object of the entire game
        """
        data = {
            "tag": self.tag,
            "name": self.name,
            "users": [user.json() for user in self.users.values()],
            "active_users": self.active_users,
            "rejoinable": self.rejoinable
        }
        return {**data, **self.game_json}

    def deactivate_user(self, user_id):
        """"
        Method to deactivate (not remove) a user in a game.
        """
        self.active_users = [u for u in self.active_users if u != user_id]

    def rejoin(self, user):
        """"
        Method to rejoin the game
        """
        self.users[user.user_id] = user
        self.active_users.append(user.user_id)

    def preview(self):
        """"
        JSON object that contains data to show in the game lobby
        """
        return {
            "tag": self.tag,
            "name": self.name,
            "min_players": self.min_players,
            "max_players": self.max_players,
        }

    @staticmethod
    def demo_action_data(data):
        """"
        Demo action
        """
        print(data)

    @staticmethod
    def demo_action():
        """"
        Demo action
        """
        pass

    def action(self, action, data):
        """"
        Handle game actions
        """
        game_action = self.actions[action]
        if game_action:
            if "data" in getfullargspec(game_action).args:
                game_action(data)
            else:
                game_action()

    def set_users(self, users):
        """"
        Set the users once a game is created
        """
        self.users = {user.user_id: user for user in users}
        self.active_users = [user.user_id for user in users]
