from datetime import datetime


class Tile(object):

    def __init__(self, value, worms):
        self.value = value
        self.worms = worms
        self.order = datetime.utcnow().timestamp()
        self.active = True

    def json(self):
        return {
            "value": self.value,
            "worms": self.worms,
            "order": self.order,
            "active": self.active,
        }
