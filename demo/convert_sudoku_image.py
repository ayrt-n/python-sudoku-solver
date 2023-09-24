import cv2 as cv
import sys
import os
project_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(project_dir)
from sudoku_solver import sudoku_image_processor
from sudoku_solver import sudoku_board
from sudoku_solver import constraint_propagation

# Example using sudoku image and converting it to an array and then solving it
# Load image from images folder
image = cv.imread('images/sudoku_1.jpg')

# Use sudoku image processor to convert image into array
sip = sudoku_image_processor.SudokuImageProcessor(image)
board = sip.convert_to_array()
print('Original Board')
for row in board:
    print(row)
print('\n---------\n')

# Use array to instantiate sudoku board
sudoku_board = sudoku_board.SudokuBoard(board)

# Solve!
solver = constraint_propagation.ConstraintPropagation(sudoku_board)
solved_board = solver.solve()[1]
print('Solved Board')
for row in solved_board:
    print(row)

# Display image of board to compare to program output
cv.imshow('Sudoku', image)
cv.waitKey(0)