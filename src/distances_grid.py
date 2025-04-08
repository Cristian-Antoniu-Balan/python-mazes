import random
from grid import Grid
import constants

class DistanceGrid(Grid):
    def __init__(self, rows, columns, mode = ''):
        super().__init__(rows, columns, mode)
        self.distances = None
        self.path = []

    def set_distances(self, distances = None):
        if distances:
            self.distances = distances
            self.path = self.get_path()

    def get_path(self):
        path = []
        if not self.distances: return path

        distance = max(self.distances.values())
        cell = list(self.distances.keys())[list(self.distances.values()).index(distance)]
        path.append(cell)

        while distance > 0:
            distance = distance - 1
            
            cells = []
            for link in path[-1].links:
                if self.distances[link] == distance:
                    cells.append(link)
            
            path.append(random.choice(cells))
            path[-1].path = True
        
        path[0].end_path = True
        path[-1].path = False
        path[-1].end_path = True

        return path



    def contents_of(self, cell):
        if self.distances and (cell in self.distances):
            match self.mode:
                case constants.MODE_DISTANCE:
                    return self.distances[cell]
                case constants.MODE_COLOR:
                    maxDistance = max(self.distances.values())
                    intensity = round(255 * (self.distances[cell] / maxDistance))
                    return intensity
                case constants.MODE_PATH:
                    self.distances[cell] if cell in self.path else ""
                    # path = self.get_path()
                    # if cell in path:
                    #     return self.distances[cell]
                    # else:
                    #     return ''
                case _:
                    return super().contents_of(cell)
            return self.distances[cell]
        else:
            return super().contents_of(cell)
 