from grid import Grid
from polar_grid import PolarGrid
from distances_grid import DistanceGrid
from recursive_backtracker import RecursiveBacktracker

from mask import Mask
from masked_grid import MaskedGrid

import constants

# print('Grid size')

# try:
#     rows = int(input('Rows: '))
#     columns = int(input('Columns: '))
#     if rows <= 0 or columns <= 0:
#         raise ValueError
# except:
#     print('Invalid input')
#     exit()

# grid = Grid(10, 10)
# grid = DistanceGrid(15, 15, constants.MODE_COLOR)
cell_size = 50
# grid = DistanceGrid(5, 5, constants.MODE_PATH)

# mask = Mask(5, 5)

# mask.set_is_enabled(0, 0, 0)
# mask.set_is_enabled(1, 2, 0)
# mask.set_is_enabled(4, 4, 0)

# mask = Mask.from_PNG('./masks/maze_in_maze.png', )
# grid = MaskedGrid(mask)

# grid = MaskedGrid(mask, constants.MODE_DISTANCE)
# print(grid.show())

# RecursiveBacktracker.on(grid)

# start = grid.get_cell(0, 0)
# start = grid.get_random_cell()
# distances = start.distances()

# grid.distances = distances.cells

# grid.generateImg(cell_size).save('./out/maze.png')

# f = open("./out/maze.svg", "w")
# f.write(grid.generateSvg(cell_size))
# f.close()

polar = PolarGrid(10, constants.MODE_PATH)
RecursiveBacktracker.on(polar)

start = polar.get_random_cell()
distances = start.distances()
polar.set_distances(distances.cells)

# for cell in polar.each_cell():
#     print(distances.cells[cell])

# for d in polar.distances:
#     print("Cell // distances RETURN >> ", d.path, d.end_path)

# polar.generateImg(cell_size).save('./out/polar.png')
mazes = polar.generateSvg(cell_size)

f = open("./out/polar.svg", "w")
f.write(mazes[0])
f.close()

f = open("./out/polar_with_color.svg", "w")
f.write(mazes[1])
f.close()

f = open("./out/polar_with_color_and_path.svg", "w")
f.write(mazes[2])
f.close()

exit()
