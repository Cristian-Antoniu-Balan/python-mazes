class Distances:
    def __init__(self, root):
        # self.root = root
        self.cells = {}
        self.cells[root] = 0
    
    def get_distance_to(self, cell):
        return self.cells[cell]
    
    def set_distance_to(self, cell, distance):
        self.cells[cell] = distance

    def get_all_cells(self):
        return self.cells.keys()
    