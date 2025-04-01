background_color_RGB = (255, 255, 255)
wall_color_RGB = (0, 0, 0)

mask_color_enabled_RGB = (255, 255, 255)

cell_size = 10
half_wall_width_ratio = 0.05

def min_cell_size(cell_size = cell_size):
    return max(2, cell_size)

def half_wall_width(cell_size = cell_size, half_wall_width_ratio = half_wall_width_ratio):
    return max(1, round(min_cell_size(cell_size) * half_wall_width_ratio))

font_color_RGB = (0, 0, 0)
font_size_ratio = 0.55