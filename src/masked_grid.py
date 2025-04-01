from cell import Cell
from grid import Grid
from mask import Mask
from distances_grid import DistanceGrid

class MaskedGrid(DistanceGrid):
    def __init__(self, mask, mode = ''):
        self.mask = mask
        super().__init__(self.mask.rows, self.mask.columns, mode)

    def prepare_grid(self):
        return [[Cell(i, j) if self.mask.get_is_enabled(i, j) else None for j in range(self.columns)] for i in range(self.rows)]

    def get_random_cell(self):
        row, column = self.mask.get_random_location()
        return self.get_cell(row, column)