from random import shuffle
from .game import Game


class Room(object):

    def __init__(self, room, password, admin):
        self.id = room
        self.password = password
        self.admin = admin.user_id
        self.users = {
            admin.user_id: admin
        }
        self.chat = []
        self.game = Game()
        self.settings = {
            "max_size": 7
        }

    @property
    def is_empty(self):
        return len(self.users) == 0

    @property
    def user_names(self):
        return [u.username for u in self.users.values()]

    @property
    def user_ids(self):
        return [u.user_id for u in self.users.values()]

    def json(self):
        return {
            "id": self.id,
            "admin": self.admin,
            "users": [u.json() for u in self.users.values()],
            "password": self.password,
            "chat": self.chat,
            "settings": self.settings,
            "game": self.game.json(),
        }

    def check_password(self, password):
        if self.password:
            return self.password == password
        return True

    def check_username(self, username):
        return username in self.user_names

    def check_user_id(self, user_id):
        return user_id in self.user_ids

    def get_user(self, user_id):
        return self.users.get(user_id, None)

    def get_user_with_sid(self, sid):
        users = {u.sid: u for u in self.users.values()}
        return users.get(sid, None)

    def can_join(self):
        return len(self.users) < self.settings["max_size"]

    def join(self, user):
        self.users[user.user_id] = user
        self.sort_users()
        # Auto rejoin game upon entering room
        # if self.game.rejoinable:
        #     self.game.rejoin(user)

    def sort_users(self):
        users = [u for u in self.users.values()]
        self.users = {
            user.user_id: user for user in sorted(users, key=lambda u: (u.user_id != self.admin, u.username))
        }

    def update_user(self, user):
        if user.user_id in self.user_ids:
            self.users[user.user_id] = user

    def remove_user(self, user_id):
        if user_id in self.users:
            del self.users[user_id]
        self.game.deactivate_user(user_id)
        self.set_random_admin()

    def set_random_admin(self):
        if self.admin not in self.users and len(self.users.keys()) > 0:
            user_ids = [u.user_id for u in self.users.values()]
            shuffle(user_ids)
            self.admin = user_ids[0]

    def update_chat(self, chat):
        self.chat.append(chat)

    def create_game(self, game, user_ids):
        self.game = game
        game.set_users([self.users[user_id] for user_id in user_ids])

    def stop_game(self):
        self.game = Game()
