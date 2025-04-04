from cell import Cell

class PolarCell(Cell):
    def __init__(self, row, column):
        super().__init__(row, column)
        self.cw = None
        self.ccw = None
        self.inward = None
        self.outward = []
    
    def neighbors(self):
        neighbors = []

        if self.cw: neighbors.append(self.cw)
        if self.ccw: neighbors.append(self.ccw)
        if self.inward: neighbors.append(self.inward)
        neighbors += self.outward

        return neighbors
