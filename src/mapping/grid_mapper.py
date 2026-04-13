import numpy as np

def create_grid(detections, frame_shape, grid_size=(40, 40)):
    grid = np.zeros(grid_size)

    height, width, _ = frame_shape

    cell_w = width / grid_size[1]
    cell_h = height / grid_size[0]

    for (x1, y1, x2, y2) in detections:

        gx1 = int(x1 / cell_w)
        gy1 = int(y1 / cell_h)
        gx2 = int(x2 / cell_w)
        gy2 = int(y2 / cell_h)

        for x in range(gx1, gx2 + 1):
            for y in range(gy1, gy2 + 1):
                if 0 <= x < grid_size[1] and 0 <= y < grid_size[0]:
                    grid[y][x] = 1

    return grid