import cv2

def draw_grid(frame, grid):
    height, width, _ = frame.shape
    rows, cols = grid.shape

    cell_w = width // cols
    cell_h = height // rows

    overlay = frame.copy()

    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == 1:
                cv2.rectangle(
                    overlay,
                    (x * cell_w, y * cell_h),
                    ((x + 1) * cell_w, (y + 1) * cell_h),
                    (0, 0, 255),
                    -1
                )

    # transparent overlay
    cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)

    return frame


def draw_path(frame, path, grid):
    height, width, _ = frame.shape
    rows, cols = grid.shape

    cell_w = width // cols
    cell_h = height // rows

    for (y, x) in path:
        cx = int(x * cell_w + cell_w / 2)
        cy = int(y * cell_h + cell_h / 2)

        cv2.circle(frame, (cx, cy), 3, (0, 255, 0), -1)

    return frame