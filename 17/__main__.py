from cmath import sqrt

def p_x(step: int, v_x: int) -> int:
    '''Returns the x-position at step and v_x as the initial x velocity. This
    function is the closed form version of x as a parametric function.'''
    c = v_x / abs(v_x) / 2
    if abs(v_x) <= step: step = v_x
    return int(-1 * pow(step, 2) * c + step * (v_x + c))

def p_y(step: int, v_y: int) -> int:
    '''Returns the y-position at step and v_y as the initial y velocity. This
    function is the closed form version of y as a parametric function.'''
    return int(step * (v_y - (step+1)/2 + 1))

def get_bounds(filename: str) -> tuple[tuple[int], tuple[int]]:
    '''Returns the bounds of the target area specified in `filename`.'''
    header = 'target area: '
    with open(filename, 'r') as f:
        line = f.readline()
        line = line[len(header):]
        x_info, y_info = line.split(', ')

        min_x, max_x = [int(x) for x in x_info[len('x='):].split('..')]
        min_y, max_y = [int(y) for y in y_info[len('y='):].split('..')]
    
    return ((min_x, max_x), (min_y, max_y))

def get_valid_steps(v_y: int, y_dest: int) -> list[int]:
    '''Returns the valid steps given v_x and y_dest from the p_y quadratic
    equuation. A valid step is defined as a real integer.'''
    a = -0.5
    b = v_y+0.5
    c = -y_dest
    d = pow(b, 2) - 4 * a * c
    t1: complex = ((-b+sqrt(d))/(2*a))
    t2: complex = ((-b-sqrt(d))/(2*a))

    def check(x: complex) -> int:
        if x.imag != 0: return None
        else: x = x.real
        
        if x <= 0: return None

        if not x.is_integer(): return None
        return x

    valid: list[int] = []

    t1 = check(t1)
    t2 = check(t2)

    if t1: valid.append(t1)
    if t2: valid.append(t2)

    return valid

def get_all_initial_velocities(x_bounds: tuple[int], y_bounds: tuple[int]) -> set[tuple[int, int]]:
    '''Returns a list of all valid initial velocities that fall in `x_bounds` and `y_bounds`.'''
    x_min, x_max = x_bounds
    y_min, y_max = y_bounds
    
    velocities: set[tuple[int, int]] = set()

    for y_dest in range(y_min, y_max+1): # loop through all y destinations
        for v_y in range(y_dest, abs(y_dest)): # loop through possible initial y velocities
            valid_steps = get_valid_steps(v_y, y_dest)
            if not valid_steps: continue

            for t in valid_steps: # loop through all valid steps
                for v_x in range(1, x_max+1): # loop through all possible v_x
                    cur_x = p_x(t, v_x)
                    if not x_min <= cur_x <= x_max: continue
                    velocities.add((v_x, v_y))
    return velocities

def main():
    x_bounds, y_bounds = get_bounds('input.txt')

    v_y = abs(y_bounds[0])-1
    height = int((v_y)*(v_y+1)/2)
    print(f'Heighest y-value possible: {height}')

    velocities = sorted(get_all_initial_velocities(x_bounds, y_bounds))
    print(f'Number of valid velocities: {len(velocities)}')

if __name__ == '__main__':
    main()