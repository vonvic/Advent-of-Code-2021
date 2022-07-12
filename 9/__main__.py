def get_low_points(height_map: tuple) -> list:
    low_points = []
    for row in range(len(height_map)):
        for col in range(len(height_map[row])):
            this_val = height_map[row][col]
            hor_low_point, vert_low_point = True, True

            if col > 0: hor_low_point &= this_val < height_map[row][col-1]
            if col < len(height_map[row])-1: hor_low_point &= this_val < height_map[row][col+1]

            if row > 0: vert_low_point &= this_val < height_map[row-1][col]
            if row < len(height_map)-1: vert_low_point &= this_val < height_map[row+1][col]

            if hor_low_point and vert_low_point:
                low_points.append(height_map[row][col]+1)
    return low_points

def get_height_map(filename: str) -> tuple:
    height_map = []
    with open(filename, 'r') as f:
        rows = [line.strip() for line in f.readlines()]
        for row in rows:
            height_map.append(tuple([int(height) for height in row]))
    return tuple(height_map)

def main():
    height_map = get_height_map('input.txt')

    low_points = get_low_points(height_map)
    print('Part One:', sum(low_points))

if __name__ == '__main__':
    main()