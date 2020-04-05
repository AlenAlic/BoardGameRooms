COLORS = ["red", "blue", "green"]
NUMBERS = [1, 2, 3]
FILLS = [0, 0.5, 1]
SHAPES = ["circle", "diamond", "square"]


class Card(object):

    def __init__(self, color=COLORS[0], number=NUMBERS[0], fill=FILLS[0], shape=SHAPES[0], placeholder=False):
        self.color = color
        self.number = number
        self.fill = fill
        self.shape = shape
        self.placeholder = placeholder

    def json(self):
        return {
            "color": self.color,
            "number": self.number,
            "fill": self.fill,
            "shape": self.shape,
            "tag": self.tag,
            "placeholder": self.placeholder
        }

    @property
    def tag(self):
        return f"{self.color}-{self.number}-{self.fill}-{self.shape}"
