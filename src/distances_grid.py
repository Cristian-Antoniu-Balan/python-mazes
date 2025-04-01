import random
from grid import Grid
import constants

class DistanceGrid(Grid):
    def __init__(self, rows, columns, mode = ''):
        super().__init__(rows, columns, mode)
        self.distances = None

    def get_path(self):
        path = []
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
                    path = self.get_path()
                    if cell in path:
                        return self.distances[cell]
                    else:
                        return ''
                case _:
                    return super().contents_of(cell)
            return self.distances[cell]
        else:
            return super().contents_of(cell)
 