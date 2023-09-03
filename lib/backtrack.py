import sudoku

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
    solution = [
        [7, 5, 6, 8, 3, 2, 1, 9, 4],
        [2, 9, 3, 4, 1, 5, 7, 8, 6],
        [1, 4, 8, 6, 9, 7, 5, 2, 3],
        [3, 8, 1, 7, 5, 4, 9, 6, 2],
        [6, 7, 4, 3, 2, 9, 8, 5, 1],
        [5, 2, 9, 1, 6, 8, 3, 4, 7],
        [4, 6, 7, 9, 8, 1, 2, 3, 5],
        [9, 1, 2, 5, 4, 3, 6, 7, 8],
        [8, 3, 5, 2, 7, 6, 4, 1, 9]
    ]
    sudoku = sudoku.Sudoku(board)
    solver = Backtrack(sudoku)
    solver.solve()

    for r in range(9):
        for c in range(9):
            if solver.sudoku.board[r][c] == solution[r][c]:
                continue
            print('ERROR')
