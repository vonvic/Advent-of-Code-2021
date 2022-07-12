def get_target_one(L: list):
    '''Returns the median of the list.'''
    from statistics import median
    return int(median(L))

def get_target_two(L: list) -> int:
    '''Returns the mean of `L` rounded down to the nearest integer.'''
    from statistics import mean
    return int(mean(L))

def calculate_fuel_one(L: list, target: int) -> int:
    '''Calculates the fuel by calcuating the absolute differences between each
    value in L and the target.'''
    from functools import reduce
    return reduce(lambda p, x: p + abs(target-x), L, 0)

def calculate_fuel_two(L: list, target: int) -> int:
    '''Calculates the fuel by getting the sum of triangle numbers, where each
    triangle number is the defined by distance between each element in `L` and
    `target`.'''
    from functools import reduce
    def f(p, x):
        diff = int(abs(x-target)+1)
        value = diff*(diff-1)//2
        return p + value
    return reduce(f, L, 0)

def get_list(file: str):
    '''Returns the list of the initial state of crab horizontal positions.'''
    with open(file, 'r') as f:
        return [int(x.strip()) for x in f.readline().split(',')]

def main():
    crabs = sorted(get_list('input.txt'))
    target = get_target_one(crabs)
    fuel = calculate_fuel_one(crabs, target)

    target_two = get_target_two(crabs)
    fuel_two = calculate_fuel_two(crabs, target_two)

    print('Part One')
    print(f'Fuel required to reposition at {target}: {fuel}')

    print()

    print('Part two')
    print(f'Fuel required to reposition at {target_two}: {fuel_two}')

if __name__ == '__main__': main()