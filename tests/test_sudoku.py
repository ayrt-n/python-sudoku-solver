from sudoku_solver.sudoku import Sudoku

class TestSudoku:
    sudoku = Sudoku([
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ])

    def test_valid_guess(self):
        self.sudoku.guess(0, 2, 9)
        assert self.sudoku.board[0][2] == 9
        assert self.sudoku.properties['row'][0][9] == True
        assert self.sudoku.properties['col'][2][9] == True
        assert self.sudoku.properties['box'][0][9] == True

    def test_invalid_guess(self):
        self.sudoku.guess(3, 0, 9)
        assert self.sudoku.board[3][0] != 9
        assert self.sudoku.properties['row'][3][9] == False
        assert self.sudoku.properties['col'][0][9] == False
        assert self.sudoku.properties['box'][3][9] == False

    def test_remove_guess(self):
        self.sudoku.guess(0, 2, 9)
        assert self.sudoku.remove_guess(0, 2) == True
        assert self.sudoku.board[0][2] == 0
        assert self.sudoku.properties['row'][0][9] == False
        assert self.sudoku.properties['col'][2][9] == False
        assert self.sudoku.properties['box'][0][9] == False

    def test_invalid_remove_guess(self):
        assert self.sudoku.remove_guess(0, 0) == False
        assert self.sudoku.board[0][0] == self.sudoku.initial_board[0][0]

    def test_is_valid_guess(self):
        assert self.sudoku.is_valid_guess(7, 7, 3) == True

    def test_is_invalid_guess(self):
        assert self.sudoku.is_valid_guess(0, 2, 7) == False
        assert self.sudoku.is_valid_guess(0, 2, 8) == False
        assert self.sudoku.is_valid_guess(0, 3, 4) == False
    
    def test_truthy_is_empty_cell(self):
        assert self.sudoku.is_empty_cell(0, 2) == True

    def test_falsy_is_empty_cell(self):
        assert self.sudoku.is_empty_cell(0, 0) == False
