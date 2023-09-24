# Python Sudoku Solver

Sudoku puzzle solver implemented in Python. Uses computer vision to read in images of sudoku boards and then solve!

## Background

While practicing leetcode problems I completed a backtracking problem related to checking the validity of sudoku boards. I enjoyed learning about backtracking and thought it would be fun to explore some of those ideas further with a small little project trying to create a sudoku solver and improving on the original backtracking solution.

While starting out by writing a simple backtracking algorithm to fully solve sudoku boards, I decided to try and improve on the time efficiency by implementing another solution which uses constraint propagation.

At the same time, I started to get more interested in computer vision and image processing and decided to add the ability to read sudoku boards from images using OpenCV and PyTesseract to convert images into arrays which could then by solved. By reading in images, users are able to save a significant amount of time, as opposed to manually filling in the boards themselves.

## How to use

I have included a few example sudoku boards within the ```images/``` directory for anyone to play around. For a quick overview of how the program works, I have included a short script ```demo/convert_sudoku_image.py``` which takes in one of the example images, converts it into an array, and then solves it.

To test it out, simply navigate to the main directory and then run:

```
python3 demo/convert_sudoku_image.py
```

The program should then print out the contents of the original board, followed by the solution:

```
Original Board
[2, 5, 0, 0, 0, 0, 4, 0, 3]
[4, 0, 0, 0, 3, 8, 2, 0, 0]
[0, 0, 3, 5, 2, 0, 0, 7, 0]
[5, 0, 6, 9, 0, 0, 0, 3, 0]
[0, 8, 0, 3, 0, 6, 0, 2, 0]
[0, 3, 0, 0, 0, 5, 7, 0, 4]
[0, 4, 0, 0, 8, 3, 1, 0, 0]
[0, 0, 1, 4, 9, 0, 0, 0, 8]
[6, 0, 8, 0, 0, 0, 0, 4, 7]

---------

Solved Board
[2, 5, 7, 1, 6, 9, 4, 8, 3]
[4, 6, 9, 7, 3, 8, 2, 1, 5]
[8, 1, 3, 5, 2, 4, 9, 7, 6]
[5, 7, 6, 9, 4, 2, 8, 3, 1]
[1, 8, 4, 3, 7, 6, 5, 2, 9]
[9, 3, 2, 8, 1, 5, 7, 6, 4]
[7, 4, 5, 6, 8, 3, 1, 9, 2]
[3, 2, 1, 4, 9, 7, 6, 5, 8]
[6, 9, 8, 2, 5, 1, 3, 4, 7]
```

## How it works

### Converting Image to Array

To convert an image of a sudoku board to an array representation, I used OpenCV (a popular image processing and computer vision library) and PyTesseract (a popular optical character recognition tool).

Without going through each step in detail; Using OpenCV, we are able to estimate which regions of the image are likely associated with sudoku cells. Using that information we can then pass the cells to PyTesseract which is then able to read the value within the cell and convert it to a value (or empty string if the cell is empty). These values are then used to populate a 2D array representation of the original sudoku board.

For more information on the details of how these images are processed and transformed, see ```sudoku_solver/sudoku_image_processor.py```.

### Solving

The backtracking algorithm effectively works by iterating through the board and trying every value (1-9) in each cell. If a certain value does not work (e.g., it hits a point where we cannot complete the board), the algorithm will then go back and try a different value in each of the spots (it backtracks!). While the algorithm is always able to find a solution to a solvable board, it is not the most optimal solution, in terms of time efficiency.

The constraint propagation algorithm works by using the information available in the starting board to continuously eliminate possible values from the other cells. The algorithm starts by looking through the starting values and eliminating those as potential values in the other cells from each of the rows/columns/boxes. After that, the algorithm will look for what are called naked doubles/triples/quads. A naked double consists of two cells in the same row/column/box that only have two possible values (triples or quads would be for cells with three or four possible values). Using that information, we know those values can only exist in those cells and we are able to eliminate those as possible values from the other cells in that row/column/box. This process continues until no more constraints are identified at which point the algorithm will solve the remainder of the puzzle using backtracking.
