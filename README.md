# Python Sudoku Solver

## Summary

While practicing leetcode problems I completed a backtracking problem related to checking the validity of sudoku boards. I enjoyed learning about backtracking and thought it would be fun to explore some of those ideas further with a small little project trying to create a sudoku solver and improving on the original backtracking solution.

While starting out by writing a simple backtracking algorithm to fully solve sudoku boards, I decided to try and improve on the time efficiency by implementing another solution which uses constraint propagation.

Backtracking effectively works by iterating through the board and trying every value (1-9) in each cell. If a certain value does not work (e.g., it hits a point where we cannot complete the board), the algorithm will then go back and try a different value in each of the spots (it backtracks!). While the algorithm is always able to find a solution to a solvable board, it is not the most optimal solution, in terms of time efficiency.

Constraint propagation works by using the information available in the starting board to continuously eliminate possible values from the other cells. The algorithm starts by looking through the starting values and eliminating those as potential values in the other cells from each of the rows/columns/boxes. After that, the algorithm will look for what are called naked doubles/triples/quads. A naked double consists of two cells in the same row/column/box that only have two possible values (triples or quads would be for cells with three or four possible values). Using that information, we know those values can only exist in those cells and we are able to eliminate those as possible values from the other cells in that row/column/box. This process continues until no more constraints are identified at which point the algorithm will solve the remainder of the puzzle using backtracking.