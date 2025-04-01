import random

class RecursiveBacktracker:
    def __init__(self):
        pass

    def on(grid = None, start_at = None):
        if grid is None: raise ValueError('Grid is required')
        if start_at is None: start_at = grid.get_random_cell()

        stack = []
        stack.append(start_at)

        while stack:
            current = stack[-1]
            neighbors = [n for n in current.neighbors() if not n.links]

            if not neighbors: stack.pop()
            else:
                neighbor = random.choice(neighbors)
                current.link(neighbor)
                stack.append(neighbor)
        
        return grid