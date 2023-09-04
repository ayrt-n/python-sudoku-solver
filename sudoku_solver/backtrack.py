class Backtrack:
    """Sudoku solver using backtracking algorithm"""
    def __init__(self, sudoku):
        self.sudoku = sudoku
    
    def solve(self):
        """
        Attempts to solve sudoku puzzle using backtracking
        Params: None
        Returns: [bool if solved, [][] of solved sudoku board]
        """
        def dfs(index):
            if index >= 81:
                return True
            
            row = index // 9
            col = index % 9

            if not self.sudoku.is_empty_cell(row, col):
                return dfs(index + 1)
            
            for val in range(1, 10):
                if not self.sudoku.is_valid_guess(row, col, val):
                    continue

                self.sudoku.guess(row, col, val)
                if dfs(index + 1):
                    return True
                self.sudoku.remove_guess(row, col)
            
            return False
        
        if dfs(0):
            return [True, self.sudoku.board]
        else:
            return [False, self.sudoku.initial_board]
