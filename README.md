# LinkedIn Queens Solver

1. Screenshot today's game
2. Pass it in to the solver like this
```bash
python solver.py path/to/screenshot
```
3. Get a png file with the solution

## Examples
### Example 1
#### Input

<p align="middle"> 
<img src="./data/1_in.jpg" alt="input" height="300"/>
</p>

#### Output
<p align="middle"> 
<img src="./data/1_in-input.png" alt="output1" width="300"/>
<img src="./data/1_in-output.png" alt="output1" width="300"/>
</p>

### Example 2
<p align="middle"> 
<img src="./data/2025-04-20-preview.png" alt="example-2" width="600"/>
</p>



### How
 - OpenCV to recognise the grid size and colours and conver them to an array
 - Backtracking solver adjusted from original n-Queens problem (this version is easier because colours are an extra contraint reducing the search space)
 - Pillow to create the output image from the array

### Environment setup
```bash
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
# python -m pip freeze > requirements.txt
# deactivate
```

### Unit tested
```bash
python -m unittest
```
