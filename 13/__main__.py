def get_points_and_folds(filename: str) -> tuple:
    '''Returns a tuple of points and folds specified in file titled `filename`.'''
    data: list

    with open(filename, 'r') as f:
        data = [line.strip() for line in f.readlines()]
    
    sep = data.index('')

    points = []
    for line in data[:sep]:
        x, y = line.split(',')
        points.append((int(x), int(y)))

    folds = []
    for line in data[sep+1:]:
        axis, position = line.split('=')
        axis = axis[-1]
        folds.append((axis, int(position)))

    return (points, folds)

def get_matrix_size_from_points(points: list[tuple]) -> tuple:
    '''Returns the (x, y) size of matrix.'''
    rows, cols = points[0]

    for x, y in points[1:]:
        cols = max(cols, x)
        rows = max(rows, y)

    return rows+1, cols+1

def default_matrix(rows: int, cols: int) -> list:
    '''Returns a matrix of size (`rows`, `cols`) with each point being a '.'.'''
    matrix = []
    for _ in range(rows):
        matrix.append(['.' for _ in range(cols)])
    return matrix

def print_matrix(matrix: list[list[str]]) -> None:
    for row in matrix: print(''.join(row))

def plot_points(matrix: list[list[str]], points: list[tuple]):
    for x, y in points: matrix[y][x] = '#'

def get_matrix_and_folds(filename: str) -> tuple:
    '''Return a tuple of (matrix, folds) where the folds is a list of all the
    folds to be made in the form of (axis, position). The matrix will be filled
    with periods, and '#' in place of points specified in `filename`.'''
    points, folds = get_points_and_folds(filename)
    rows, cols = get_matrix_size_from_points(points)
    matrix = default_matrix(rows, cols)
    plot_points(matrix, points)
    return matrix, folds

def get_size_points_folds(filename: str) -> tuple:
    '''Return a tuple of (matrix, folds) where the folds is a list of all the
    folds to be made in the form of (axis, position). The matrix will be filled
    with periods, and '#' in place of points specified in `filename`.'''
    points, folds = get_points_and_folds(filename)
    get_matrix_size_from_points(points)
    return set(points), folds

def get_reflection(point: tuple, fold: tuple):
    '''Returns the reflection of `point` at the line specifed at `fold`.'''
    axis, position = fold
    x, y = point
    match axis:
        case 'x': return (2*position-x, y)
        case 'y': return (x, 2*position-y)
        case _: raise ValueError(f'Unknown axis: {axis}')

def simulate_folding(points: list, folds: list):
    '''Simulates the folding and returns the number of points left. The folding
    is done by finding the reflection of a point only on one side.'''
    points = set(points)

    for fold in folds:
        axis, position = fold
        new_points = set() # gather new points after folding each point
        for point in points:
            x, y = point
            new_point: tuple = point
            match axis:
                case 'x':
                    if x > position: new_point = (get_reflection(point, fold))
                case 'y':
                    if y > position: new_point = (get_reflection(point, fold))
                case _: raise ValueError(f'Unknown axis: {axis}')
            new_points.add(new_point)
        points = new_points
    return points

def main():
    points, folds = get_size_points_folds('input.txt')
    new_points_first_fold = simulate_folding(points, folds[:1])
    print(f'Number of visible dots after the first fold: {len(new_points_first_fold)}')

    new_points = simulate_folding(points, folds)
    rows, cols = get_matrix_size_from_points(list(new_points))
    matrix = default_matrix(rows, cols)
    plot_points(matrix, new_points)
    print_matrix(matrix)

if __name__ == '__main__':
    main()