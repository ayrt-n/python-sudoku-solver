class ConstraintPropagation:
    """Sudoku solver using constraint propagation algorithm"""
    def __init__(self, sudoku):
        self.sudoku = sudoku
        self.generate_constraints()

    def solve(self):
        """
        Attempts to solve sudoku puzzle by using constraint propagation and backtracking (DFS)
        Params: None
        Returns [bool if solved, [][] of solved sudoku board]
        """
        progress = [True]
        while any(progress):
            progress = [self.propagate_single_constraints(),
                        self.propagate_row_constraints(),
                        self.propagate_col_constraints(),
                        self.propagate_box_constraints()]
        
        if self.sudoku.is_complete():
            return [True, self.sudoku.board]
        elif self.dfs(0):
            return [True, self.sudoku.board]
        else:
            return [False, self.sudoku.initial_board]

    def dfs(self, index):
        """
        Attempts to solve sudoku using DFS and iterating through the constraints matrix for possible values
        Params: index (int)
        Returns: bool if solved
        """
        if index >= 81:
            return True
        
        row = index // 9
        col = index % 9

        if not self.sudoku.is_empty_cell(row, col):
            return self.dfs(index + 1)
        
        for val in self.constraints[row][col]:
            if not self.sudoku.is_valid_guess(row, col, val):
                continue
            self.sudoku.guess(row, col, val)
            if self.dfs(index + 1):
                return True
            self.sudoku.remove_guess(row, col)

        return False
    
    def propagate_single_constraints(self):
        """
        Iterate through constraints matrix to find cells with only one possible value. Fill in those values and propagate the constraint
        Params: None
        Returns: bool if changes made (e.g., single value constraint found that has not been filled in)
        """
        changes_made = False

        for r in range(9):
            for c, constraint in enumerate(self.constraints[r]):
                if (len(constraint) > 1 or not self.sudoku.is_empty_cell(r, c) or not
                    self.sudoku.is_valid_guess(r, c, list(constraint)[0])):
                    continue
                changes_made = True
                self.sudoku.guess(r, c, list(constraint)[0])
                self.propagate_single_constraint(constraint, r, c)
        
        return changes_made
    
    def propagate_row_constraints(self):
        """
        Iterate through rows looking for naked sets (doubles, triples, quads) and propagate constraint if found
        Params: None
        Returns: bool if change made (e.g., naked set found and propagating the constraint changed other constraints)
        """
        changes_made = False

        for row in range(9):
            sets = {}
            for col in range(9):
                if frozenset(self.constraints[row][col]) in sets:
                    sets[frozenset(self.constraints[row][col])] += 1
                sets[frozenset(self.constraints[row][col])] = 1

            for constraint, count in sets.items():
                num_constraints = len(constraint)
                if (num_constraints < 2 or num_constraints > 4 or num_constraints != count):
                    continue
                if self.propagate_row_constraint(constraint, row):
                    changes_made = True

        return changes_made
    
    def propagate_col_constraints(self):
        """
        Iterate through columns looking for naked sets (doubles, triples, quads) and propagate constraint if found
        Params: None
        Returns: bool if change made (e.g., naked set found and propagating the constraint changed other constraints)
        """
        changes_made = False

        for col in range(9):
            sets = {}
            for row in range(9):
                if frozenset(self.constraints[row][col]) in sets:
                    sets[frozenset(self.constraints[row][col])] += 1
                sets[frozenset(self.constraints[row][col])] = 1

            for constraint, count in sets.items():
                num_constraints = len(constraint)
                if (num_constraints < 2 or num_constraints > 4 or num_constraints != count):
                    continue
                if self.propagate_col_constraint(constraint, row):
                    changes_made = True

        return changes_made

    def propagate_box_constraints(self):
        """
        Iterate through boxes looking for naked sets (doubles, triples, quads) and propagate constraint if found
        Params: None
        Returns: bool if change made (e.g., naked set found and propagating the constraint changed other constraints)
        """
        changes_made = False
        box_ranges = [range(0, 3), range(3, 6), range(6, 9)]

        for rows in box_ranges:
            for cols in box_ranges:
                sets = {}
                for row in rows:
                    for col in cols:
                        if frozenset(self.constraints[row][col]) in sets:
                            sets[frozenset(self.constraints[row][col])] += 1
                        sets[frozenset(self.constraints[row][col])] = 1

                for constraint, count in sets.items():
                    num_constraints = len(constraint)
                    if (num_constraints < 2 or num_constraints > 4 or num_constraints != count):
                        continue
                    if self.propagate_box_constraint(constraint, row):
                        changes_made = True

        return changes_made

    def propagate_single_constraint(self, constraint, row, col):
        """
        Takes a constraint and propagates it across the row, column, and box associated with the constraint
        Params: constraint (set), row (int), col (int)
        Returns: None
        """
        self.propagate_row_constraint(constraint, row)
        self.propagate_col_constraint(constraint, col)
        self.propagate_box_constraint(constraint, row, col)

    def propagate_row_constraint(self, constraint, row):
        """
        Takes constraint and removes these potential values from other cells within the same row
        E.g., constraint { 1, 2 } from row [{ 1, 2 }, { 1, 2 }, { 1, 2, 3 }] => [{ 1, 2 }, { 1, 2 }, { 3 }]
        Params: constraint (set), row (int)
        Returns: bool if any changes made
        """
        changes_made = False

        for c in range(9):
            if (self.constraints[row][c] == constraint or not any(self.constraints[row][c] & constraint)):
                continue
            changes_made = True
            self.constraints[row][c] -= constraint

        return changes_made
    
    def propagate_col_constraint(self, constraint, col):
        """
        Takes constraint and removes these potential values from other cells within the same column
        E.g., constraint { 1, 2 } from column [{ 1, 2 }, { 1, 2 }, { 1, 2, 3 }] => [{ 1, 2 }, { 1, 2 }, { 3 }]
        Params: constraint (set), col (int)
        Returns: bool if any changes made
        """
        changes_made = False

        for r in range(9):
            if (self.constraints[r][col] == constraint or not any(self.constraints[r][col] & constraint)):
                continue
            changes_made = True
            self.constraints[r][col] -= constraint
        
        return changes_made

    def propagate_box_constraint(self, constraint, row, col):
        """
        Takes constraint and removes these potential values from other cells within the same box
        E.g., constraint { 1, 2 } from box [{ 1, 2 }, { 1, 2 }, { 1, 2, 3 }] => [{ 1, 2 }, { 1, 2 }, { 3 }]
        Params: constraint (set), row (int), col (int)
        Returns: bool if any changes made
        """
        changes_made = False
        box_row_start = (row // 3) * 3
        box_col_start = (col // 3) * 3

        for r in range(box_row_start, box_row_start + 3):
            for c in range(box_col_start, box_col_start + 3):
                if (self.constraints[r][c] == constraint or not any(self.constraints[r][c] & constraint)):
                    continue
                changes_made = True
                self.constraints[r][c] -= constraint
        
        return changes_made

    def generate_constraints(self):
        """
        Generate initial constraints matrix based on filled in values of sudoku board and create instance variable constraints
        Params: None
        Returns: None
        """
        self.constraints = []
        for r in range(9):
            row = []
            for c in range(9):
                if self.sudoku.board[r][c] == 0:
                    row.append({ 1, 2, 3, 4, 5, 6, 7, 8, 9 })
                else:
                    row.append({ self.sudoku.board[r][c] })
            self.constraints.append(row)
        
        for r in range(9):
            for c, constraint in enumerate(self.constraints[r]):
                if len(constraint) > 1:
                    continue
                self.propagate_single_constraint(constraint, r, c)
