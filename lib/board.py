import copy

class Sudoku:
    """Class representation of sudoku board. Used to check whether guess is valid and keep track of guesses."""

    def __init__(self, board):
        # Create board, initial board, and board properties instance variables
        self.board = board
        self.initial_board = [[v for v in row] for row in board]
        self.properties = self.create_board_properties(board)
    
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
    for row in sudoku.properties['box']:
        print(row)

