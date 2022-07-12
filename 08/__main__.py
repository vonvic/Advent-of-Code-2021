SEGMENT_COUNT = 7
DIGIT_0 = frozenset({0, 1, 2, 4, 5, 6})
DIGIT_1 = frozenset({2, 5})
DIGIT_2 = frozenset({0, 2, 3, 4, 6})
DIGIT_3 = frozenset({0, 2, 3, 5, 6})
DIGIT_4 = frozenset({1, 2, 3, 5})
DIGIT_5 = frozenset({0, 1, 3, 5, 6})
DIGIT_6 = frozenset({0, 1, 3, 4, 5, 6})
DIGIT_7 = frozenset({0, 2, 5})
DIGIT_8 = frozenset({0, 1, 2, 3, 4, 5, 6})
DIGIT_9 = frozenset({0, 1, 2, 3, 5, 6})

segments_to_digits = {
    DIGIT_0 : 0,
    DIGIT_1 : 1,
    DIGIT_2 : 2,
    DIGIT_3 : 3,
    DIGIT_4 : 4,
    DIGIT_5 : 5,
    DIGIT_6 : 6,
    DIGIT_7 : 7,
    DIGIT_8 : 8,
    DIGIT_9 : 9
}

def get_signal_patterns(file: str) -> list:
    '''Returns a collection of signal patterns retrieved in from file called
    `file`.'''
    with open(file, 'r') as f:
        data = []
        for line in [line.strip() for line in f.readlines()]:
            patterns, output = line.split(' | ')
            patterns, output = patterns.split(' '), output.split(' ')
            data.append((tuple(patterns), tuple(output)))
        return data

def filter_table_with_segments(segments_table, signal_pattern, digit):
    for segment in digit:
        segments_table[segment] = segments_table[segment] & set(signal_pattern)

def filter_final(segments_table: dict):
    definite_letters: set = set()
    next_loop_needed = True
    while next_loop_needed:
        next_loop_needed = False

        # get new definite letters
        for possibilities in segments_table.values():
            if len(possibilities) == 1:
                letter = ''.join(possibilities)
                if letter not in definite_letters:
                    definite_letters.add(letter)
                    next_loop_needed = True
        
        # filter rest
        for segment in segments_table.keys():
            if len(segments_table[segment]) != 1:
                new = segments_table[segment] - definite_letters
                if new != segments_table[segment]:
                    segments_table[segment] = new
                    next_loop_needed = True

def default_table() -> dict:
    SEGMENT_LABELS = range(SEGMENT_COUNT)
    all_possibilities_for_each_segment = [set('abcdefg') for _ in range(SEGMENT_COUNT)]
    return dict(zip(SEGMENT_LABELS, all_possibilities_for_each_segment))

def decode_table(signals: tuple):
    '''Returns a decode table based on `signals`.'''
    segments_table = default_table()

    for pattern in signals:
        segment_count = len(pattern)
        match segment_count:
            case 2: filter_table_with_segments(segments_table, pattern, DIGIT_1)
            case 4: filter_table_with_segments(segments_table, pattern, DIGIT_4)
            case 3: filter_table_with_segments(segments_table, pattern, DIGIT_7)
            case 7: filter_table_with_segments(segments_table, pattern, DIGIT_8)
            case 6:
                digits = DIGIT_0 & DIGIT_6  & DIGIT_9
                filter_table_with_segments(segments_table, pattern, digits)
            case 5:
                digits = DIGIT_2 & DIGIT_3 & DIGIT_5
                filter_table_with_segments(segments_table, pattern, digits)
            case _: pass
    filter_final(segments_table)
    return {''.join(v): k for k, v in segments_table.items()}

def count_1_4_7_8_only(signal_patterns):
    '''Returns a dictionary with the count of 1s, 4s, 7s, and 8s in
    `signal_patterns`.'''
    count = {1: 0, 4: 0, 7: 0, 8: 0}
    for _, output in signal_patterns:
        for pattern in output:
            match len(pattern):
                case 2: count[1] += 1
                case 4: count[4] += 1
                case 3: count[7] += 1
                case 7: count[8] += 1
    return count

def get_digit(table: dict, pattern: str) -> int:
    '''Decodes pattern into a digit based on `table`.'''
    segments = set()
    for signal in pattern:
        segments.add(table[signal])

    return segments_to_digits[frozenset(segments)]

def convert_to_number(digits) -> int:
    '''Converts a list of digits into an integer.'''
    number = 0
    for digit in digits:
        number = number*10 + digit
    return number

def decode_patterns(signal_patterns):
    '''Returns a list of numbers decoded from the signal patterns.'''
    numbers = []
    for sequences, output in signal_patterns:
        table = decode_table(sequences)
        number = []
        for output_pattern in output:
            number.append(get_digit(table, output_pattern))
        numbers.append(convert_to_number(number))
    return numbers

def main():
    signal_patterns = get_signal_patterns('input.txt')
    part_one_count = count_1_4_7_8_only(signal_patterns)
    print('Part One:', sum(part_one_count.values()))

    numbers = decode_patterns(signal_patterns)
    print('Part two:', sum(numbers))
if __name__ == '__main__':
    main()