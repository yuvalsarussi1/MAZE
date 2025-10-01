[README.md](https://github.com/user-attachments/files/22644602/README.2.md)
# Maze Solver in Python

This project implements a maze solver using Python, NumPy, and PIL.  
It takes maze images, preprocesses them into binary arrays, and automatically finds and visualizes the solution path.

## Project Structure

```
.
├── Maze.py                 # Image-based maze solver (converts + solves)
├── MazeTerminal.py         # Terminal-based solver with ASCII visualization
├── MazePhoto.jpg           # Original maze image
├── Screenshot_5.png        # Example terminal solved maze
├── tmpkn1t03k3.PNG         # Example image solved maze
```

## Features

- Image Preprocessing: Converts raw images into one-pixel-wide mazes using pixel averaging.  
- Pathfinding Algorithm: Custom recursive solver to navigate and solve the maze.  
- Terminal Representation: ASCII/colored block output in the terminal.  
- Image Output: Highlights the solution path in green on the maze image.  
- Works across different maze sizes (20x20, 40x40, 150x150, etc.).
- for the 40x40 and 150x150 images make sure you change the size of the terminal so the mazed will be printed 

## Usage

### 1. Run the terminal solver
```bash
python MazeTerminal.py
```
This prints the maze in the terminal with the solution path.

### 2. Run the image solver
```bash
python Maze.py
```
This opens the solved maze image with the solution highlighted in green.

## Examples

### Terminal Solved Maze  
![Terminal Maze Output](Screenshot_5.png)  

### Image Solved Maze  
![Photo Maze Output](tmpkn1t03k3.PNG)  

## Recursive Pathfinding Algorithm

The solver works recursively, exploring paths step by step:

1. Check Available Moves (Offsets)  
   - From the current pixel (x, y), the algorithm looks in all four directions (up, down, left, right).  
   - Valid moves are added to a list of directions.  

2. Single Path (Straight Corridor)  
   - If there is only one valid direction, the algorithm keeps walking forward automatically.  
   - This avoids unnecessary recursive calls in hallways.  

3. Multiple Paths (Node Creation)  
   - If there are two or more possible moves, a node is created.  
   - The node stores the current position, parent coordinates, and remaining possible directions.  
   - Each direction is then explored recursively.  

4. Dead End or Exit  
   - If there are no valid moves, recursion ends.  
   - If the exit is reached, the full path is stored as a solution.  

## Project Notes

- The Maze.py file takes a raw image and converts it into a one-pixel-wide maze using pixel averaging, then draws the solved path directly on the processed image.  
- The MazeTerminal.py file works with the ready-to-use one-pixel maze and represents it in the terminal.  
- I built everything from scratch, including the recursive algorithm.  
- I first experimented with recursion while working on my Chess Engine project, and this maze solver helped me refine and build a working recursive approach.

## Requirements

- Python 3.x  
- NumPy  
- Pillow (PIL)  

Install with:  
```bash
pip install numpy pillow
```

