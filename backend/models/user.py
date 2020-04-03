

class User(object):

    def __init__(self, username, sid, user_id=None):
        self.username = username
        self.user_id = f"{username}_{sid}" if user_id is None else user_id
        self.sid = sid

    def json(self):
        return {
            "username": self.username,
            "user_id": self.user_id,
            "sid": self.sid,
        }
