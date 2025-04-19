
import sys
import numpy as np
from utils import image_to_grid_array_auto, grid_array_to_png
from datetime import datetime

QUEEN_VALUE = -1

class Solver:
    def __init__(self, path):
        self.palette, self.arr = image_to_grid_array_auto(path)
        assert len(self.palette) == len(self.arr)

    def place(self, row, matrix, colors):
        n = len(matrix)

        if row == n:
            return True
        
        for col in range(n):            
            if self.isSafe(row, col, matrix) and not matrix[row][col] in colors:
                colour = matrix[row][col]
                matrix[row][col] = QUEEN_VALUE
                colors.add(colour)
                if self.place(row+1, matrix, colors):
                    return True
                matrix[row][col] = colour
                colors.remove(colour)
        return False

    def isSafe(self, row, col, matrix):
        n = len(matrix)

        # check uppen col
        for i in range(row):
            if matrix[i][col] == QUEEN_VALUE:
                return False

        # check diagonals
        if col-1 >= 0 and matrix[row-1][col-1] == QUEEN_VALUE:
            return False
        if col+1 < n and matrix[row-1][col+1] == QUEEN_VALUE:
            return False
        
        return True


    def solve(self, out_path):
        colors = set()
        matrix = [[x for x in y] for y in self.arr]

        # If the solution exists
        if self.place(0, matrix, colors):
            grid_array_to_png(self.arr, self.palette, output_path=f"{out_path}-input.png")
            grid_array_to_png(matrix, self.palette, output_path=f"{out_path}-output.png")
            return [row.index(-1) for row in matrix], matrix
        else:
            return None, matrix

if __name__ == "__main__":
    if len( sys.argv ) != 2:
        print("Requires image input")
        exit()
    solver = Solver(sys.argv[1])
    solved_at = datetime.now()
    solution, _ = solver.solve(f"data/{solved_at}")
    if solution is not None:
        print("solved")
    else:
        print("failed")

