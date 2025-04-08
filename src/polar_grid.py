import math
from PIL import Image, ImageDraw, ImageFont, ImageColor

from distances_grid import DistanceGrid
from polar_cell import PolarCell
import constants
import defaults

class PolarGrid(DistanceGrid):
    def __init__(self, rows, mode = ''):
        super().__init__(rows, 1, mode = mode)
    
    def prepare_grid(self):
        rows = [None for i in range(self.rows)]

        row_height = 1 / self.rows
        rows[0] = [PolarCell(0, 0)]

        for row in range(self.rows):
            if row == 0: continue
            radius = row / self.rows
            circumference = 2 * math.pi * radius

            previous_count = len(rows[row - 1])
            estimated_cell_width = circumference / previous_count
            ratio = round(estimated_cell_width / row_height)

            cells = previous_count * ratio

            rows[row] = [PolarCell(row, col) for col in range(cells)]
        
        return rows
    
    def configure_cells(self):
        for cell in self.each_cell():
            row = cell.row
            col = cell.column

            if row > 0:
                col_cw = (col + 1) if col < len(self.grid[row]) - 1 else 0
                col_ccw = (col - 1) if col > 0 else len(self.grid[row]) - 1
                cell.cw = self.grid[row][col_cw]
                cell.ccw = self.grid[row][col_ccw]

                ratio = len(self.grid[row]) / len(self.grid[row - 1])
                parent = self.grid[row - 1][int(col / ratio)]
                parent.outward = [cell]
                cell.inward = parent

    def cell_coords(self, cell, cell_size = defaults.cell_size, half_wall_width = defaults.half_wall_width(defaults.cell_size), center = 0):
        # (-1) to mirror ImageDraw...arc() >> cw becomes positive
        theta = (-1) * 2 * math.pi / len(self.grid[cell.row])
        inner_radius = (cell.row * cell_size) / 2
        outer_radius = ((cell.row + 1) * cell_size) / 2
        theta_cw = cell.column * theta
        theta_ccw = (cell.column + 1) * theta
        half_wall_width = half_wall_width

        ax = int(center + (inner_radius * math.cos(theta_ccw)))
        ay = int(center + (inner_radius * math.sin(theta_ccw)))
        bx = int(center + (outer_radius * math.cos(theta_ccw)))
        by = int(center + (outer_radius * math.sin(theta_ccw)))
        cx = int(center + (inner_radius * math.cos(theta_cw)))
        cy = int(center + (inner_radius * math.sin(theta_cw)))
        dx = int(center + (outer_radius * math.cos(theta_cw)))
        dy = int(center + (outer_radius * math.sin(theta_cw)))

        xm = int(center + ((inner_radius + outer_radius) / 2) * math.cos((theta_ccw + theta_cw) / 2))
        ym = int(center + ((inner_radius + outer_radius) / 2) * math.sin((theta_ccw + theta_cw) / 2))

        if cell.row == 0:
            xm = int(center)
            ym = int(center)

        return [ax, ay, bx, by, cx, cy, dx, dy, xm, ym, inner_radius, outer_radius, theta_ccw, theta_cw, theta]
    
    def generateImg(self, cell_size = defaults.cell_size):
        cell_size = defaults.min_cell_size(cell_size)
        background_color = defaults.background_color_RGB
        wall_color = defaults.wall_color_RGB
        half_wall_width = defaults.half_wall_width(cell_size)
        font_size = defaults.font_size_ratio * cell_size / 2
        font_color = defaults.font_color_RGB
    
        height = cell_size * self.rows
        width = height

        img = Image.new('RGBA', (width, height), background_color)
        font = ImageFont.truetype('arial', font_size)
        def color(intensity = 0):
            return (ImageColor.getrgb('blue') + (intensity,))
        
        def drawCell(ax = 0, ay = 0, bx = 0, by = 0, cx = 0, cy = 0, dx = 0, dy = 0, xm = 0, ym = 0, theta_ccw = 0, theta_cw = 0, width = 2 * half_wall_width, color = wall_color, fill_color = wall_color):
            ImageDraw.Draw(img).line((ax, ay, bx, by), color, 2 * half_wall_width)
            ImageDraw.Draw(img).line((cx, cy, dx, dy), color, 2 * half_wall_width)
            ImageDraw.Draw(img).arc(inner_arc_bounding_box, math.degrees(theta_ccw), math.degrees(theta_cw), color, 2 * half_wall_width)
            ImageDraw.Draw(img).arc(outer_arc_bounding_box, math.degrees(theta_ccw), math.degrees(theta_cw), color, 2 * half_wall_width)
            # ImageDraw.floodfill(img, (xm, ym), (255, 0, 0))
        
        ImageDraw.Draw(img).circle([width / 2, width / 2], width / 2, None, wall_color, 2 * half_wall_width)

        for cell in self.each_cell():
            if cell is None: continue
            if cell.row == 0: continue
            # half_wall_width / 2 >> correction for how ImageDraw..line handles stroke side ??
            [ax, ay, bx, by, cx, cy, dx, dy, xm, ym, inner_radius, outer_radius, theta_ccw, theta_cw, theta] = self.cell_coords(cell, cell_size, 0, width / 2)

            inner_arc_bounding_box = [(width / 2 - inner_radius),
                                      (width / 2 - inner_radius),
                                      (width / 2 + inner_radius),
                                      (width / 2 + inner_radius)]

            outer_arc_bounding_box = [(width / 2 - outer_radius),
                                      (width / 2 - outer_radius),
                                      (width / 2 + outer_radius),
                                      (width / 2 + outer_radius)]
            
            if not cell.is_linked(cell.inward):
                ImageDraw.Draw(img).arc(inner_arc_bounding_box, math.degrees(theta_ccw), math.degrees(theta_cw), wall_color, 2 * half_wall_width)
            
            if not cell.is_linked(cell.cw):
                ImageDraw.Draw(img).line((ax, ay, bx, by), wall_color, 2 * half_wall_width)

            # fix these for polar coordinates
            match self.mode:
                case constants.MODE_DISTANCE | constants.MODE_PATH:
                    if self.mode == constants.MODE_PATH and self.contents_of(cell) == 0:
                        drawCell(ax, ay, bx, by, cx, cy, dx, dy, xm, ym, theta_ccw, theta_cw, color = 'RGB(255, 0, 0)', fill_color=(255, 0, 0))
                    ImageDraw.Draw(img).text((xm, ym), f'{self.contents_of(cell)}', font_color, font, 'mm', 1, 'center')
                # case constants.MODE_COLOR:
                #     ImageDraw.Draw(img).rectangle((x1, y1, x2, y2),color(self.contents_of(cell)))
                #     # define a better way to find start and end cells
                #     if self.contents_of(cell) == 0:
                #         ImageDraw.Draw(img).text((xm, ym), '0', 'red', font, 'mm', 1, 'center')
                #     if self.contents_of(cell) == 255:
                #         ImageDraw.Draw(img).text((xm, ym), '1', 'red', font, 'mm', 1, 'center')
                case _:
                    pass
        ImageDraw.Draw(img).rectangle((width / 2 - 10, width / 2 - 10, width / 2 + 10, width / 2 + 10), None, 'blue', 4)
        ImageDraw.floodfill(img, xy=(width / 2, width / 2), value=(255, 0, 0), thresh=200)
        return img
    
    def generateSvg(self, cell_size = defaults.cell_size):
        cell_size = defaults.min_cell_size(cell_size)
        half_wall_width = defaults.half_wall_width(cell_size)
        background_color = defaults.background_color_RGB
        wall_color = defaults.wall_color_RGB
        fill_color_end_path = (144, 238, 144)
        fill_color_path = (173, 216, 230)

        total_height = cell_size * self.rows + 2 * half_wall_width
        total_width = total_height

        def line(x1 = 0, y1 = 0, x2 = 0, y2 = 0, width = 2 * half_wall_width, color = wall_color):
            return f"<line x1=\"{x1}\" y1=\"{y1}\" x2=\"{x2}\" y2=\"{y2}\" stroke-width=\"{width}\" stroke=\"RGB{color}\" />"
        
        def arc(x_start = 0, y_start = 0, rx = 0, ry = 0, x_end = 0, y_end = 0, width = 2 * half_wall_width, color = wall_color):
            return f"<path d=\"M {x_start} {y_start} A {rx} {ry} 0 0 1 {x_end} {y_end}\" fill=\"None\" stroke-width=\"{width}\" stroke=\"RGB{color}\" />"

        def cell_filled(ax = 0, ay = 0, bx = 0, by = 0, cx = 0, cy = 0, dx = 0, dy = 0, inner_radius = 0, outer_radius = 0, width = 2 * half_wall_width, color = wall_color, fill_color = wall_color):
            return f"""<path d=\"
                            M {ax} {ay}
                            A {inner_radius} {inner_radius} 0 0 1 {cx} {cy}
                            L {dx} {dy}
                            A {outer_radius} {outer_radius} 0 0 0 {bx} {by}
                            Z\"
                    fill=\"RGB{fill_color}\" stroke-width=\"{width}\" stroke=\"RGB{color}\" />"""

        def cell_center_filled(cx = 0, cy = 0, r = 0, width = 2 * half_wall_width, color = wall_color, fill_color = wall_color):
            return f"<circle cx=\"{cx}\" cy=\"{cy}\" r=\"{r}\" fill=\"RGB{fill_color}\" stroke-width=\"{width}\" stroke=\"RGB{color}\"/>"
        
        def cell_text(x = 0, y = 0, text = ""):
            return f"<text x=\"{x}\" y=\"{y}\" text-anchor=\"middle\" alignment-baseline=\"central\">{text}</text>"
        
        header = [f"<svg height=\"{total_height}\" width=\"{total_width}\" xmlns=\"http://www.w3.org/2000/svg\">"]
        background = f"<rect width=\"100%\" height=\"100%\" fill=\"RGB{background_color}\"/>"
        outer_circle = f"<circle cx=\"{total_width / 2}\" cy=\"{total_width / 2}\" r=\"{total_width / 2}\" fill=\"None\" stroke-width=\"{2 * half_wall_width}\" stroke=\"RGB{wall_color}\"/>"
        header.append(background)
        header.append(outer_circle)
        
        maze = []
        layer_color = []
        layer_path = []


        for cell in self.each_cell():
            if cell is None: continue

            [ax, ay, bx, by, cx, cy, dx, dy, xm, ym, inner_radius, outer_radius, theta_ccw, theta_cw, theta] = self.cell_coords(cell, cell_size, 0, total_width / 2)

            match self.mode:
                case constants.MODE_DISTANCE | constants.MODE_PATH:
                    if self.mode == constants.MODE_PATH and (cell.path or cell.end_path):
                        fill_color = fill_color_path if cell.path else fill_color_end_path

                        layer_path.append(cell_text(xm, ym, self.contents_of(cell)))
                        if cell.row == 0:
                            layer_color.append(cell_center_filled(xm, ym, outer_radius, 0, fill_color=fill_color))
                            continue
                        else:
                            layer_color.append(cell_filled(ax, ay, bx, by, cx, cy, dx, dy, inner_radius, outer_radius, width=0, fill_color=fill_color))
                # case constants.MODE_COLOR:
                #     ImageDraw.Draw(img).rectangle((x1, y1, x2, y2),color(self.contents_of(cell)))
                #     # define a better way to find start and end cells
                #     if self.contents_of(cell) == 0:
                #         ImageDraw.Draw(img).text((xm, ym), '0', 'red', font, 'mm', 1, 'center')
                #     if self.contents_of(cell) == 255:
                #         ImageDraw.Draw(img).text((xm, ym), '1', 'red', font, 'mm', 1, 'center')
                case _:
                    pass

            if not cell.is_linked(cell.inward): maze.append(arc(ax, ay, inner_radius, inner_radius, cx, cy))
            if not cell.is_linked(cell.cw): maze.append(line(ax, ay, bx, by))

        maze_with_color = layer_color + maze
        maze_with_color_and_path = maze_with_color + layer_path
        mazes = []
        for data in [maze, maze_with_color, maze_with_color_and_path]:
            file = header + data
            file.append(f"</svg>")
            mazes.append("\n".join(file)) 

        return mazes