import cv2
import numpy as np
from collections import OrderedDict
from PIL import Image

def detect_grid_size(warped_bin, mult=0.2):
    """
    Given a binary (0/255) top‑down view of the grid (black lines on white),
    return (N, cell_size), where N is the number of cells per row/col
    and cell_size is the pixel spacing between adjacent lines.
    """
    # 1) vertical projection to find x‐positions of the lines
    proj_x = np.sum(warped_bin, axis=0)            # sum over y
    thresh = mult * proj_x.max()                   # pick a high threshold
    line_idxs = np.where(proj_x > thresh)[0]       # columns that belong to lines

    # 2) cluster consecutive indices into individual lines
    splits = np.where(np.diff(line_idxs) > 1)[0] + 1
    groups = np.split(line_idxs, splits)
    x_coords = np.array([g.mean() for g in groups])

    # The number of cells is (# lines – 1)
    N = len(x_coords) - 1

    # cell spacing is the median distance between consecutive line‑coords
    cell_size = int(np.median(np.diff(x_coords)))

    return N, cell_size

def image_to_grid_array_auto(image_path, warp_size=800):
    # — same preprocessing, find largest 4‑corner contour, do the warp —
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    th = cv2.adaptiveThreshold(blur, 255,
                               cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY_INV,
                               11, 2)
    # find grid border contour (as before) …
    cnts, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    grid_cnt = None
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02*peri, True)
        if len(approx) == 4:
            grid_cnt = approx
            break
    if grid_cnt is None:
        raise RuntimeError("Grid border not found")

    # warp to square
    pts = grid_cnt.reshape(4,2)
    s = pts.sum(axis=1); diff = np.diff(pts, axis=1).reshape(4)
    rect = np.zeros((4,2), dtype="float32")
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    dst = np.array([[0,0],[warp_size-1,0],[warp_size-1,warp_size-1],[0,warp_size-1]], 
                   dtype="float32")
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(img, M, (warp_size, warp_size))
    cv2.imwrite("data/result.png", warped)

    # make a binary grid‐line image to detect lines
    warped_gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    _, warped_bin = cv2.threshold(warped_gray, 128, 255, cv2.THRESH_BINARY_INV)

    # detect N and cell_size
    N, cell = detect_grid_size(warped_bin)

    # print(N, cell)
    
    palette = OrderedDict()

    # now chop into N×N cells, sampling only the interior 80%
    margin = int(cell * 0.4)
    grid = np.zeros((N, N), dtype=np.uint8)
    for r in range(N):
        for c in range(N):
            y0, y1 = r*cell + margin, (r+1)*cell - margin
            x0, x1 = c*cell + margin, (c+1)*cell - margin
            patch = warped[y0:y1, x0:x1]

            avg_color = tuple([int(x) for x in patch.reshape(-1,3).mean(axis=0).astype(int)])
            # print(avg_color)
            if avg_color not in palette:
                palette[avg_color] = len(palette)
            grid[r, c] = palette[avg_color]

    return palette, [[int(x) for x in y] for y in grid]

def grid_array_to_png(grid_array, palette, cell_size=50, border=2, output_path='grid.png'):
    """
    Turn an array into an image of colored blocks
    and save it as a PNG.
    - grid_array: shape (x,x), values in 0–255 (int)
    - cell_size: pixel size of each square
    - output_path: where to save the PNG
    """
    colors = list(palette.items())
    rows = len(grid_array)
    cols = rows

    # total image size includes border on all sides of every cell
    width  = cols * cell_size + (cols + 1) * border
    height = rows * cell_size + (rows + 1) * border

    # start with a black background
    img = Image.new('RGB', (width, height), (0, 0, 0))

    for r in range(rows):
        for c in range(cols):
            color = colors[grid_array[r][c]][0] if grid_array[r][c]>=0 else 'black'
            block = Image.new('RGB', (cell_size, cell_size), color)

            x = border + c * (cell_size + border)
            y = border + r * (cell_size + border)
            img.paste(block, (x, y))
    img.save(output_path)
    return output_path

# Usage example (assuming you already have `arr`):
# png_file = grid_array_to_png(arr, cell_size=60, output_path='/mnt/data/mygrid.png')
# print("Saved grid image to", png_file)


if __name__ == "__main__":
    palette, arr = image_to_grid_array_auto("data/0_input.png")
    grid_array_to_png(arr, palette, output_path="data/0_output.png")

    palette, arr = image_to_grid_array_auto("data/1_in_sq.png")
    grid_array_to_png(arr, palette, output_path="data/1_in_sq_out.png")

    palette, arr = image_to_grid_array_auto("data/1_in.jpg")
    grid_array_to_png(arr, palette, output_path="data/1_in_out.png")

    # arr[0][0] = -1
    # print(palette)
    # print(np.array(arr))
