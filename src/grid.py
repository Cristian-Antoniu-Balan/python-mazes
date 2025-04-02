import random
from PIL import Image, ImageDraw, ImageFont, ImageColor

from cell import Cell
import constants
import defaults

class Grid:
    def __init__(self, rows, columns, mode = ''):
        self.rows = rows
        self.columns = columns
        self.grid = self.prepare_grid()
        self.configure_cells()
        self.mode = mode

    def prepare_grid(self):
        grid = []
        for row in range(self.rows):
            currentRow = []
            for column in range(self.columns):
                currentRow.append(Cell(row, column))
            grid.append(currentRow)
        return grid
    
    def configure_cells(self):
        for row in range(self.rows):
            for column in range(self.columns):
                cell = self.grid[row][column]
                if cell is None: continue
                if row > 0: cell.north = self.grid[row - 1][column]
                if row < (self.rows - 1): cell.south = self.grid[row + 1][column]
                if column < (self.columns - 1) : cell.east = self.grid[row][column + 1]
                if column > 0: cell.west = self.grid[row][column - 1]
    
    def get_cell(self, row, column):
        if 0 <= row < self.rows and 0 <= column < self.columns:
            return self.grid[row][column]
        else:
            return None
        
    def get_random_cell(self):
        row = random.randrange(0, self.rows, 1)
        column = random.randrange(0, len(self.grid[row]), 1)

        return self.grid[row][column]
    
    def each_row(self):
        for row in range(self.rows):
            yield self.grid[row]
    
    def each_cell(self):
        for row in self.each_row():
            for cell in row:
                yield cell
    
    def contents_of(self, cell):
        return ''
    
    def size(self):
        return self.rows * self.columns

    def show(self):
        for row in range(self.rows):
            for column in range(self.columns):
                end = ' ' if column < self.columns - 1 else '\r\n'
                print(self.grid[row][column].show() if self.grid[row][column] else 'X,X', end=end)
    
    def cell_coords(self, cell, cell_size = defaults.cell_size, half_wall_width = defaults.half_wall_width(defaults.cell_size)):
            x1 = cell.column * cell_size + half_wall_width
            y1 = cell.row * cell_size + half_wall_width
            x2 = (cell.column + 1) * cell_size + half_wall_width
            y2 = (cell.row + 1) * cell_size + half_wall_width
            xm = (x1 + x2) / 2
            ym = (y1 + y2) / 2

            return [x1, x2, y1, y2, xm, ym]
    
    def generateImg(self, cell_size = defaults.cell_size):
        cell_size = defaults.min_cell_size(cell_size)
        background_color = defaults.background_color_RGB
        wall_color = defaults.wall_color_RGB
        half_wall_width = defaults.half_wall_width(cell_size)
        font_size = defaults.font_size_ratio * cell_size
        font_color = defaults.font_color_RGB
    
        width = cell_size * self.columns + 2 * half_wall_width
        height = cell_size * self.columns + 2 * half_wall_width

        img = Image.new('RGBA', (width, height), background_color)
        font = ImageFont.truetype('arial', font_size)
        def color(intensity = 0):
            return (ImageColor.getrgb('blue') + (intensity,))

        for cell in self.each_cell():
            if cell is None: continue
            # half_wall_width / 2 >> correction for how ImageDraw..line handles stroke side ??
            [x1, x2, y1, y2, xm, ym] = self.cell_coords(cell, cell_size, half_wall_width / 2)

            match self.mode:
                case constants.MODE_DISTANCE | constants.MODE_PATH:
                    if self.mode == constants.MODE_PATH and self.contents_of(cell) == 0:
                        ImageDraw.Draw(img).rectangle((x1, y1, x2, y2),color(255))
                    ImageDraw.Draw(img).text((xm, ym), f'{self.contents_of(cell)}', font_color, font, 'mm', 1, 'center')
                case constants.MODE_COLOR:
                    ImageDraw.Draw(img).rectangle((x1, y1, x2, y2),color(self.contents_of(cell)))
                    # define a better way to find start and end cells
                    if self.contents_of(cell) == 0:
                        ImageDraw.Draw(img).text((xm, ym), '0', 'red', font, 'mm', 1, 'center')
                    if self.contents_of(cell) == 255:
                        ImageDraw.Draw(img).text((xm, ym), '1', 'red', font, 'mm', 1, 'center')        
                case _:
                    pass

            if cell.north is None: ImageDraw.Draw(img).line((x1, y1, x2, y1), wall_color, 2 * half_wall_width)
            if cell.west is None: ImageDraw.Draw(img).line((x1, y1, x1, y2), wall_color, 2 * half_wall_width)

            if not cell.is_linked(cell.east): ImageDraw.Draw(img).line((x2, y1, x2, y2), wall_color, 2 * half_wall_width)
            if not cell.is_linked(cell.south): ImageDraw.Draw(img).line((x1, y2, x2, y2), wall_color, 2 * half_wall_width)

        return img
    
    def generateSvg(self, cell_size = defaults.cell_size):
        cell_size = defaults.min_cell_size(cell_size)
        half_wall_width = defaults.half_wall_width(cell_size)
        background_color = defaults.background_color_RGB
        wall_color = defaults.wall_color_RGB

        total_width = cell_size * self.columns + 2 * half_wall_width
        total_height = cell_size * self.rows + 2 * half_wall_width

        def line(x1 = 0, y1 = 0, x2 = 0, y2 = 0, width = 2 * half_wall_width, color = wall_color):
            return f"<line x1=\"{x1}\" y1=\"{y1}\" x2=\"{x2}\" y2=\"{y2}\" stroke-width=\"{width}\" stroke=\"RGB{color}\" />"
        
        background = f"<rect width=\"100%\" height=\"100%\" fill=\"RGB{background_color}\"/>"

        data = [f"<svg height=\"{total_height}\" width=\"{total_width}\" xmlns=\"http://www.w3.org/2000/svg\">"]
        data.append(background)

        for cell in self.each_cell():
            if cell is None: continue

            [x1, x2, y1, y2, *rest] = self.cell_coords(cell, cell_size, half_wall_width)

            if cell.north is None: data.append(line(x1, y1, x2, y1))
            if cell.west is None: data.append(line(x1, y1, x1, y2))

            if not cell.is_linked(cell.east): data.append(line(x2, y1, x2, y2))
            if not cell.is_linked(cell.south): data.append(line(x1, y2, x2, y2))

        data.append(f"</svg>")

        return "\n".join(data)