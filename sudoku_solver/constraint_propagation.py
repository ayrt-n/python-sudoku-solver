import sudoku

class ConstraintPropagation:
    def __init__(self, sudoku):
        self.sudoku = sudoku
        self.generate_constraints(sudoku)

    def propagate_single_constraint(self, constraint, row, col):
        self.propagate_row_constraint(constraint, row)
        self.propagate_col_constraint(constraint, col)
        self.propagate_box_constraint(constraint, row, col)

    def propagate_row_constraint(self, constraint, row):
        changes_made = False

        for c in range(9):
            if (self.constraints[row][c] == constraint or not any(self.constraints[row][c] & constraint)):
                continue
            changes_made = True
            self.constraints[row][c] -= constraint

        return changes_made
    
    def propagate_col_constraint(self, constraint, col):
        changes_made = False

        for r in range(9):
            if (self.constraints[r][col] == constraint or not any(self.constraints[r][col] & constraint)):
                continue
            changes_made = True
            self.constraints[r][col] -= constraint
        
        return changes_made

    def propagate_box_constraint(self, constraint, row, col):
        changes_made = True
        box_row_start = (row // 3) * 3
        box_col_start = (col // 3) * 3

        for r in range(box_row_start, box_row_start + 3):
            for c in range(box_col_start, box_col_start + 3):
                if (self.constraints[r][c] == constraint or not any(self.constraints[r][c] & constraint)):
                    continue
                changes_made = True
                self.constraints[r][c] -= constraint
        
        return changes_made

    def generate_constraints(self, sudoku):
        self.constraints = []
        for r in range(9):
            row = []
            for c in range(9):
                if sudoku.board[r][c] == 0:
                    row.append({ 1, 2, 3, 4, 5, 6, 7, 8, 9 })
                else:
                    row.append({ sudoku.board[r][c] })
            self.constraints.append(row)
        
        for r in range(9):
            for c, constraint in enumerate(self.constraints[r]):
                if len(constraint) > 1:
                    continue
                self.propagate_single_constraint(constraint, r, c)

if __name__ == '__main__':
    board = [
        [0, 0, 0, 8, 3, 2, 0, 9, 0],
        [0, 0, 0, 0, 0, 5, 7, 0, 6],
        [1, 0, 0, 6, 0, 0, 0, 0, 0],
        [3, 0, 0, 0, 0, 0, 0, 0, 0],
        [6, 7, 4, 0, 0, 0, 8, 5, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 7],
        [0, 0, 0, 0, 0, 1, 0, 0, 5],
        [9, 0, 2, 5, 0, 0, 0, 0, 0],
        [0, 3, 0, 2, 7, 6, 0, 0, 0]
    ]
    sudoku = sudoku.Sudoku(board)
    solver = ConstraintPropagation(sudoku)
    for row in solver.constraints:
        print(row)
