def count_increases(depths: list):
    '''Returns the number of times the depth increases from a previous
    measurement.'''
    count = 0
    for i in range(1, len(depths)):
        prev, curr = depths[i-1], depths[i]

        if (curr-prev) > 0: count += 1
    return count

if __name__ == '__main__':
    depths: list
    with open('input.txt', 'r') as f:
        depths = [int(line.strip()) for line in f.readlines()]
    increase_count = count_increases(depths)
    print(f'Increase count: {increase_count}')
