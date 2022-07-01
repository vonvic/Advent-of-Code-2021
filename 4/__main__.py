def check_win(board: list, loc: tuple):
    '''Checks the board for a win at `loc`. The win is determiend if all'''
    row, col = loc
    win_horizontal, win_vertically = True, True
    for k in range(5):
        if board[row][k] != 'X':
            win_horizontal = False
            break
    for k in range(5):
        if board[k][col] != 'X':
            win_vertically = False
            break
    return win_horizontal or win_vertically

def get_location(board: list, value: int) -> tuple:
    '''Returns tuple (row, col) of the location of `value` in the `board`. If
    the value does not exist, then return None.'''
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == value: return (row, col)
    return None

def mark_board(board: list, loc: tuple) -> None:
    '''Marks the board at `loc` with an 'X'.'''
    row, col = loc
    board[row][col] = 'X'

def find_board(boards: list, drawings: list) -> tuple:
    '''Returns the winning board based on the drawings'''
    current_drawings = []
    for drawing in drawings:
        current_drawings.append(drawing)
        for board in boards:
            location = get_location(board, drawing)
            if not location: continue
            mark_board(board, location)
            if check_win(board, location):
                return (board, current_drawings.pop())

    return (None, None)

def get_sum_unmarked(board: list) -> int:
    '''Returns the sum of '''
    s = 0
    for row in board:
        for val in row:
            if val != 'X': s += val
    return s

if __name__ == '__main__':
    drawings: list
    boards = []

    with open('input.txt', 'r') as f:
        drawings = [int(x) for x in f.readline().split(',')]
        f.readline()

        board = []
        for line in f.readlines():
            line = line.strip()
            if line:
                board.append([int(x) for x in filter(lambda x: x, line.split(' '))])
            else:
                boards.append(board)
                board = []
    
    board, winning_number = find_board(boards, drawings)
    sum_unmarked = get_sum_unmarked(board)
    print(f'Board: {board}')
    print(f'Sum of uncalled numbers: {sum_unmarked}')
    print(f'Winning number: {winning_number}')
    print(f'Multiplied: {sum_unmarked*winning_number}')