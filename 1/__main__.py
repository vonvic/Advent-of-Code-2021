
def count_increases(depths: list, width: int = 0):
    '''Returns the number of times the sum of depths increases from a previous
    measurement. The sum of depths is specified from the `width` argument.'''
    count = 0
    for i in range(1, len(depths)):
        prev, curr = sum(depths[i-1:i-1+width+1]), sum(depths[i:i+width+1])
        if (curr-prev) > 0: count += 1
    return count

if __name__ == '__main__':
    depths: list
    with open('input.txt', 'r') as f:
        depths = [int(line.strip()) for line in f.readlines()]
    increase_count = count_increases(depths, 2)
    print(f'Increase count: {increase_count}')
