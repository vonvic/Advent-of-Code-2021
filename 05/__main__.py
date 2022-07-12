def get_dimensions(segments: list) -> tuple:
    '''Returns the minimum dimensions of the segments by finding the maximum
    x and y values from the segments list.'''
    max_x, max_y = 0, 0

    for segment in segments:
        one, two = segment
        x1, y1 = one
        x2, y2 = two
        max_x, max_y = max(max_x, x1, x2), max(max_y, y1, y2)
    
    return (max_x+1, max_y+1)

def get_segments(lines: list):
    '''Returns a list of segments parsed as a list of pair of points, where each
    point is a tuple of (x,y).'''
    def convert_to_tuple(x: str):
        one, two = [y.strip() for y in x.split('->')]
        return (tuple([int(z) for z in one.split(',')]), tuple([int(z) for z in two.split(',')]))

    segments = [convert_to_tuple(x.strip()) for x in lines]
    return segments

def build_matrix(dimensions: tuple) -> list:
    '''Builds a matrix based on `dimensions`, each entry with a value of 0.'''
    x, y = dimensions
    matrix = []
    for _ in range(y):
        matrix.append([0 for _ in range(x)])
    return matrix

def lay_segments(segments: list, matrix: list) -> None:
    '''Lays the segments specified by `segments` onto `matrix`.'''
    for segment in segments:
        one, two = segment
        x1, y1 = one
        x2, y2 = two

        if x1 == x2: # vertical
            for i in range(abs(y2-y1)+1): matrix[min(y1,y2)+i][x1] += 1
        elif y1 == y2: # horizontal
            for i in range(abs(x2-x1)+1): matrix[y1][min(x1,x2)+i] += 1
        else: # diagonal
            x_delta = 1 if x2 > x1 else -1
            y_delta = 1 if y2 > y1 else -1
            for i in range(abs(y2-y1)+1): matrix[y1+y_delta*i][x1+x_delta*i] += 1
            pass

def output_matrix(matrix: list, out_name: str):
    '''Outputs `matrix` into a file called `out_name`.'''
    with open(out_name, 'w') as f:
        for row in matrix:
            f.write(' '.join([str(x) for x in row]) + '\n')

def get_overlapping_count(matrix: list) -> int:
    '''Counts the number of overlapping points in `matrix`, where an overlapping
    point has value greater than 1 in `matrix`.'''
    count = 0
    for row in matrix:
        for val in row:
            if val > 1: count += 1
    return count

if __name__ == '__main__':
    segments: list
    with open('input.txt', 'r') as f:
        segments = get_segments(f.readlines())
    dimensions = get_dimensions(segments)
    matrix = build_matrix(dimensions)
    lay_segments(segments, matrix)
    output_matrix(matrix, 'matrix.txt')
    overlapping_count = get_overlapping_count(matrix)
    print(f'Number of points overlapping: {overlapping_count}')