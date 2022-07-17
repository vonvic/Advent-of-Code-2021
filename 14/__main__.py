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
    pairs_freq = {pair: 0 for pair in rules.keys()}
    for i, v in enumerate(template[:-1]):
        pair = v + template[i+1]
        pairs_freq[pair] += 1
    
    letter_freq = {letter : template.count(letter) for letter in set(template)}
    for _ in range(N):
        new_freq = {pair: 0 for pair in rules.keys()}
        for pair, freq in pairs_freq.items():
            if freq == 0: continue

            c = rules[pair]
            l, r = pair
            new_freq[l+c] += freq
            new_freq[c+r] += freq

            letter_freq[c] = letter_freq.get(c, 0) + freq
        pairs_freq = new_freq
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