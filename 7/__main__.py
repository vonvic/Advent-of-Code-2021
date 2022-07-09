def median(L: list):
    '''Returns the median.'''
    if len(L) % 2 == 0:
        ind1, ind2 = len(L)//2-1, len(L)//2
        return (L[ind1] + L[ind2])//2
    else:
        return L[len(L)//2-1]

def calculate_fuel(L: list, target: int) -> int:
    '''Calculates the fuel by calcuating the absolute differences between each
    value in L and the target.'''
    from functools import reduce
    return reduce(lambda p, x: p + abs(target-x), L, 0)

def get_list(file: str):
    '''Returns the list of the initial state of crab horizontal positions.'''
    with open(file, 'r') as f:
        return [int(x.strip()) for x in f.readline().split(',')]

def main():
    crabs = sorted(get_list('input.txt'))
    target = median(crabs)
    fuel = calculate_fuel(crabs, target)

    print(f'Fuel required to reposition at {target}: {fuel}')

if __name__ == '__main__': main()