import random
from PIL import Image

class Mask:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.enabled = [[True for i in range(self.columns)] for j in range(self.rows)]

    def get_is_enabled(self, row, column):
        if 0 <= row < self.rows and 0 <= column < self.columns:
            return self.enabled[row][column]
        else:
            return False
        
    def set_is_enabled(self, row, column, is_enabled):
        if is_enabled in [0, 1]:
            self.enabled[row][column] = is_enabled
        else:
            pass

    def get_random_location(self):
        while True:
            row = random.randrange(0, self.rows, 1)
            column  = random.randrange(0, self.columns, 1)

            if self.enabled[row][column]:
                return (row, column)
            
    def from_PNG(file):
        masked_color_enabled = (0, 0, 0)

        image = Image.open(file).convert("RGB")
        pixels = image.load()

        mask = Mask(image.height, image.width)

        for row in range(mask.rows):
            for column in range(mask.columns):
                if pixels[column, row] == masked_color_enabled:
                    mask.set_is_enabled(row, column, 1)
                else:
                    mask.set_is_enabled(row, column, 0)
        
        return mask
