def get_template_and_rules(filename: str) -> tuple:
    '''Returns (template, rules) where the template is first line of the file
    called `filename`, and rules is the rest of the lines in that file
    (excluding the blank line).'''
    template: str
    rules = dict()
    with open(filename, 'r') as f:
        template = f.readline().strip()
        f.readline() # blank line
        for rule in f.readlines():
            k, v = rule.split(' -> ')
            rules[k] = v.strip()
    return (template, rules)

def get_freq_table_after_running(template: str, rules: dict, N: int):
    '''Returns the frequency of all the letters in the final string after
    running `template` against `rules` for `N` times.'''
    from collections import Counter
    from itertools import pairwise
    pairs_freq = Counter(map(''.join, pairwise(template)))
    
    letter_freq = Counter(template)
    for _ in range(N):
        new_counter = Counter()
        for pair, freq in pairs_freq.items():
            c = rules[pair]
            l, r = pair
            new_counter[l+c] += freq
            new_counter[c+r] += freq
            letter_freq[c] += freq
        pairs_freq = new_counter
    return letter_freq

def get_most_and_least_count(freq: dict) -> tuple[int, int]:
    '''Returns the frequencies of the most frequent and least frequent items in
    `freq`.'''
    most_freq, least_freq = max(freq, key=freq.get), min(freq, key=freq.get)
    return freq[most_freq], freq[least_freq]

def main():
    template, rules = get_template_and_rules('input.txt')
    N = 10
    freq = get_freq_table_after_running(template, rules, N)
    most, least = get_most_and_least_count(freq)
    print('Part One:', most-least)   

    N = 40
    freq = get_freq_table_after_running(template, rules, N)
    most, least = most, least = get_most_and_least_count(freq)
    print('Part Two:', most-least)

if __name__ == '__main__':
    main()