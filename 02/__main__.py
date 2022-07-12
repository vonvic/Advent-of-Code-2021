def run_moves(moves: list) -> tuple:
    '''Starting at depth 0 and horizontal position 0, returns the final depth
    and horizontal positions after executing all moves contained in `moves`.'''
    depth = 0
    hor_pos = 0
    aim = 0

    for move in moves:
        direction, distance = move
        match direction:
            case 'forward':
                hor_pos += distance
                depth += distance * aim
            case 'up':
                aim -= distance
            case 'down':
                aim += distance
            case _:
                raise ValueError(f'Unknown direction {direction}')
    return (depth, hor_pos)

def convert_to_tuple(s: str):
    '''Converts a line of text from an input file into a tuple of direction and
    distance, where distance is a number.'''
    direction, distance = s.strip().split(' ')
    return (direction, int(distance))

if __name__ == '__main__':
    moves: list
    with open('input.txt', 'r') as f:
        moves = [convert_to_tuple(line) for line in f.readlines()]
    depth, horizontal_position = run_moves(moves)

    print(f'Depth: {depth}')
    print(f'Horizontal position: {horizontal_position}')
    print(f'Multiplied: {depth*horizontal_position}')