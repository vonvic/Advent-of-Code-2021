_OPT = dict()

def simulate_lantern_fish(days_left: int, timer: int, timer_start: int):
    '''Returns the number of lantern fish that exist after `days_left` pass by
    for a single lantern fish that births a new lantern fish after timer runs down to
    -1. Once the a baby is birthed, the timer restarts to timer_start to 6 days.
    Each baby has a timer_start of 8 days.'''
    param = (days_left, timer, timer_start)
    if param in _OPT: return _OPT[param] # retrieve prev. saved value from memoization

    if days_left == -1:
        return 1

    if timer == -1: # birth new baby
        curr_timer_start = 6
        baby_timer_start = 8
        curr = simulate_lantern_fish(days_left-1, curr_timer_start-1, curr_timer_start)
        baby = simulate_lantern_fish(days_left-1, baby_timer_start-1, baby_timer_start)

        _OPT[param] = curr + baby
        return _OPT[param]
    else: # run down the timer and continue on days
        _OPT[param] = simulate_lantern_fish(days_left-1, timer-1, timer_start)
        return _OPT[param]

def get_list(file: str):
    '''Returns the list of the initial state of lantern fish.'''
    with open(file, 'r') as f:
        return [int(x.strip()) for x in f.readline().split(',')]

def main():
    lantern_fishes = get_list('input.txt')

    total = 0
    timer_start = 6
    days_left = 256

    for fish in lantern_fishes:
        total += simulate_lantern_fish(days_left, fish, timer_start)

    print('Total:', total)

if __name__ == '__main__':
    main()