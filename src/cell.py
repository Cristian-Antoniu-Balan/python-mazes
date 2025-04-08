from distances import Distances

class Cell:
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.links = {}
        self.north = None
        self.south = None
        self.east = None
        self.west = None
        self.end_path = False
        self.path = False
    
    def show(self):
        return f'{self.row},{self.column}'
    
    def link(self, cell, biDirectional = True):
        self.links[cell] = True
        if biDirectional: cell.link(self, False)
        return self

    def unlink(self, cell, biDirectional = True):
        del self.links[cell]
        if biDirectional: cell.unlink(self, False)
        return self
    
    def links(self):
        return (self.links.keys())

    def is_linked(self, cell):
        return cell in self.links
    
    def neighbors(self):
        neighbors = []
        if self.north: neighbors.append(self.north)
        if self.south: neighbors.append(self.south)
        if self.east: neighbors.append(self.east)
        if self.west: neighbors.append(self.west)
        return neighbors
    
    def distances(self):
        distances = Distances(self)
        frontier = [self]

        while frontier:
            new_frontier = []

            for cell in frontier:
                for linked in cell.links:
                    if linked in distances.cells: continue
                    distances.cells[linked] = distances.cells[cell] + 1
                    new_frontier.append(linked)

            frontier = new_frontier

        return distances