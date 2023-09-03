class Sudoku:
    """Class representation of sudoku board"""

    def __init__(self, board):
        """
        Initialize sudoku instance
        Params: board ([][] of int)
        Returns: None
        """
        self.board = board
        self.initial_board = [[v for v in row] for row in board]
        self.properties = self.create_board_properties(board)
    
    def guess(self, row, col, value):
        """
        Insert value on board and update board properties
        Params: row (int), col (int), value (int)
        Returns: bool whether successful
        """
        if self.initial_board[row][col] > 0:
            return False
        
        if self.board[row][col] > 0:
            self.remove_guess(row, col)
        
        self.board[row][col] = value
        self.properties['row'][row][value] = True
        self.properties['col'][col][value] = True
        self.properties['box'][3 * (row // 3) + (col // 3)][value] = True

    def remove_guess(self, row, col):
        """
        Remove value from board and board properties
        Params: row (int), col (int)
        Returns: bool if successful
        """
        if self.initial_board[row][col] > 0:
            return False
        
        value = self.board[row][col]
        self.board[row][col] = 0
        self.properties['row'][row][value] = False
        self.properties['col'][col][value] = False
        self.properties['box'][3 * (row // 3) + (col // 3)][value] = False
        return True

    def is_valid_guess(self, row, col, value):
        """
        Check if guess is valid (e.g., value does not exist yet in row/col/box)
        Params: row (int), col (int), value (int)
        Returns: bool if guess is valid
        """
        if (self.properties['row'][row][value] or
                self.properties['col'][col][value] or
                self.properties['box'][3 * (row // 3) + (col // 3)][value]):
            return False
        
        return True
    
    def is_empty_cell(self, row, col):
        """
        Check if cell if empty
        Params: row (int), col (int)
        Returns: bool if cell is empty
        """
        return self.board[row][col] == 0

    def reset_board(self):
        """
        Reset board and properties to the intitial board
        Params: None
        Returns: None
        """
        self.board = [[v for v in row] for row in self.initial_board]
        self.properties = self.create_board_properties(self.initial_board)

    def create_board_properties(self, board):
        """
        Create properties hash for easy lookup and validation of guesses made in each row, col, or box
        Params: board ([][] of int)
        Returns: {}
        """
        properties = {}
        properties['row'], properties['col'], properties['box'] = [[False for v in range(10)] for i in range(9)], [[False for v in range(10)] for i in range(9)], [[False for v in range(10)] for i in range(9)]

        for r in range(9):
            for c, val in enumerate(board[r]):
                if val == 0:
                    continue

                b = 3 * (r // 3) + (c // 3)
                properties['row'][r][val], properties['col'][c][val], properties['box'][b][val] = True, True, True

        return properties

if __name__ == '__main__':
    board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]
    sudoku = Sudoku(board)

    for row in sudoku.board:
        print(row)
