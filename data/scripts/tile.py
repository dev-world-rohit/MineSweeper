class Tile:
    def __init__(self, x, y, image_type):
        self.x = x
        self.y = y
        self.type = image_type
        self.discovered = False
        self.flagged = False

    def discover_tile(self):
        self.discovered = True

    def switch_flagged(self):
        self.flagged = False if self.flagged else True
