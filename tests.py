import unittest
import os
import shutil
from solver import Solver
from parameterized import parameterized
from utils import image_to_grid_array_auto, grid_array_to_png

class TestSolver(unittest.TestCase):

    @parameterized.expand([
        ("data/0_input.png", [7, 3, 0, 6, 1, 5, 2, 4]),        # Test case 1
        ("data/2025-04-20.jpeg", [8, 3, 7, 2, 5, 1, 6, 4, 0]),        # Test case 2
        ("data/1_in_sq.png", [0, 8, 5, 2, 4, 7, 3, 6, 1, 9]),  # Test case 3
        ("data/1_in.jpg", [0, 8, 5, 2, 4, 7, 3, 6, 1, 9]),     # Test case 4
        ("data/2_in.jpg", [0, 6, 8, 5, 1, 9, 2, 4, 7, 3]),     # Test case 5
    ])
    def test_can_solve_grid(self, input_path, expected):
        test_dir = "data/test_output"
        # shutil.rmtree(test_dir)  # Delete the directory and all its contents
        # os.mkdir(test_dir)
        solver = Solver(input_path)
        solution, _ = solver.solve(f"{test_dir}/{input_path[5:-4]}")
        assert solution == expected

    @parameterized.expand([
        ("data/0_input.png", 8),      # Test case 1
        ("data/2025-04-20.jpeg", 9),  # Test case 2
        ("data/1_in_sq.png", 10),     # Test case 3
        ("data/1_in.jpg", 10),        # Test case 4
        ("data/2_in.jpg", 10),        # Test case 5
    ])
    def test_can_convert_image_to_grids_of_different_sizes(self, input_path, size):
        ## from image to grid
        palette, arr = image_to_grid_array_auto(input_path)

        assert len(palette) == size
        assert len(arr) == size
        assert len(arr[0]) == size

        out_path = "data/0_test_out.png"
        assert not os.path.exists(out_path)

        ## back to an image
        grid_array_to_png(arr, palette, output_path=out_path)
        assert os.path.exists(out_path)

        palette2, arr2 = image_to_grid_array_auto(input_path)

        assert len(palette2) == size
        assert len(arr2) == size
        assert len(arr2[0]) == size  
        os.remove(out_path)  # Delete the file

if __name__ == '__main__':
    unittest.main()
