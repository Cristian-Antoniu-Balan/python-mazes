import math
from PIL import Image, ImageDraw, ImageFont, ImageColor

from grid import Grid
import constants
import defaults

class PolarGrid(Grid):
    def __init__(self, rows, columns, mode = ''):
        super().__init__(rows, columns, mode)

    def cell_coords(self, cell, cell_size = defaults.cell_size, half_wall_width = defaults.half_wall_width(defaults.cell_size), center = 0):
        theta = 2 * math.pi / len(self.grid[cell.row])
        inner_radius = cell.row * cell_size
        outer_radius = (cell.row + 1) * cell_size
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

        xm = (ax + bx + cx + dx) / 4
        ym = (ay + by + cy + dy) / 4

        return [ax, ay, bx, by, cx, cy, dx, dy, xm, ym, inner_radius, outer_radius, theta_ccw, theta_cw, theta]
    
    def generateImg(self, cell_size = defaults.cell_size):
        cell_size = defaults.min_cell_size(cell_size)
        background_color = defaults.background_color_RGB
        wall_color = defaults.wall_color_RGB
        # half_wall_width = defaults.half_wall_width(cell_size)
        font_size = defaults.font_size_ratio * cell_size
        font_color = defaults.font_color_RGB
    
        # width = cell_size * self.columns + 2 * half_wall_width
        # height = cell_size * self.columns + 2 * half_wall_width
        
        width = cell_size * self.columns
        height = cell_size * self.columns

        img = Image.new('RGBA', (width, height), background_color)
        font = ImageFont.truetype('arial', font_size)
        def color(intensity = 0):
            return (ImageColor.getrgb('blue') + (intensity,))

        ImageDraw.Draw(img).circle([width / 2, width / 2], width / 2, None, (255, 0, 255))

        for cell in self.each_cell():
            if cell is None: continue
            # half_wall_width / 2 >> correction for how ImageDraw..line handles stroke side ??
            [ax, ay, bx, by, cx, cy, dx, dy, xm, ym, inner_radius, outer_radius, theta_ccw, theta_cw, theta] = self.cell_coords(cell, cell_size, 0, width / 2)

            # fix these for polar coordinates
            # match self.mode:
            #     case constants.MODE_DISTANCE | constants.MODE_PATH:
            #         if self.mode == constants.MODE_PATH and self.contents_of(cell) == 0:
            #             ImageDraw.Draw(img).rectangle((x1, y1, x2, y2),color(255))
            #         ImageDraw.Draw(img).text((xm, ym), f'{self.contents_of(cell)}', font_color, font, 'mm', 1, 'center')
            #     case constants.MODE_COLOR:
            #         ImageDraw.Draw(img).rectangle((x1, y1, x2, y2),color(self.contents_of(cell)))
            #         # define a better way to find start and end cells
            #         if self.contents_of(cell) == 0:
            #             ImageDraw.Draw(img).text((xm, ym), '0', 'red', font, 'mm', 1, 'center')
            #         if self.contents_of(cell) == 255:
            #             ImageDraw.Draw(img).text((xm, ym), '1', 'red', font, 'mm', 1, 'center')        
            #     case _:
            #         pass

            # if cell.north is None: ImageDraw.Draw(img).line((x1, y1, x2, y1), wall_color, 2 * half_wall_width)
            # if cell.west is None: ImageDraw.Draw(img).line((x1, y1, x1, y2), wall_color, 2 * half_wall_width)

            arc_bounding_box = [(width - inner_radius) / 2,
                                (width - inner_radius) / 2,
                                (width + inner_radius) / 2,
                                (width + inner_radius) / 2]
            # arc_start_angle_deg = theta_ccw * 360
            # arc_end_angle_deg = theta_cw * 360

            if cell.row == 1 and cell.column == 0:
                ImageDraw.Draw(img).circle([ax, ay], 2, None, (255, 0, 255))
                ImageDraw.Draw(img).circle([bx, by], 2, None, (255, 0, 255))
                ImageDraw.Draw(img).circle([cx, cy], 2, None, (255, 0, 255))
                ImageDraw.Draw(img).circle([dx, dy], 2, None, (255, 0, 255))
            
            if not cell.is_linked(cell.north):
                # ImageDraw.Draw(img).line((ax, ay, bx, by), wall_color)
                ImageDraw.Draw(img).arc(arc_bounding_box, math.degrees(theta_cw), math.degrees(theta_ccw), (255, 0, 0))
            else:
                ImageDraw.Draw(img).arc(arc_bounding_box, math.degrees(theta_cw), math.degrees(theta_ccw), (255, 200, 50))
            if not cell.is_linked(cell.east):
                # ImageDraw.Draw(img).arc(arc_bounding_box, math.degrees(theta_ccw), math.degrees(theta_cw), (255, 0, 0))
                ImageDraw.Draw(img).line((ax, ay, bx, by), wall_color)
            else:
                ImageDraw.Draw(img).line((ax, ay, bx, by), (255, 200, 50))

        return img