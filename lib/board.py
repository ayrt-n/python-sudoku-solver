import copy

class Sudoku:
    """Class representation of sudoku board. Used to check whether guess is valid and keep track of guesses."""

    # Takes 2D array of board and creates board, initial board, and board properties instance variables
    def __init__(self, board):
        self.board = board
        self.initial_board = [[v for v in row] for row in board]
        self.properties = self.create_board_properties(board)
    
    # Insert value on board and update board properties - Return bool if successful
    def guess(self, row, col, value):
        if self.initial_board[row][col] > 0:
            return False
        
        if self.board[row][col] > 0:
            self.remove_guess(row, col)
        
        self.board[row][col] = value
        self.properties['row'][row][value] = True
        self.properties['col'][col][value] = True
        self.properties['box'][3 * (row // 3) + (col // 3)][value] = True

    def remove_guess(self, row, col):
        if self.initial_board[row][col] > 0:
            return False
        
        value = self.board[row][col]
        self.board[row][col] = 0
        self.properties['row'][row][value] = False
        self.properties['col'][col][value] = False
        self.properties['box'][3 * (row // 3) + (col // 3)][value] = False

    # Takes board and returns hash containing properties of board for easy validation of row, col, and box values
    def create_board_properties(self, board):
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
    sudoku.guess(0, 2, 9)
    print(sudoku.properties['row'][0])

    for row in sudoku.board:
        print(row)

    sudoku.remove_guess(0, 2)
    print(sudoku.properties['row'][0])

    for row in sudoku.board:
        print(row)