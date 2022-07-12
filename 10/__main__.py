MATCH_TABLE = {
    '(' : ')',
    '[' : ']',
    '{' : '}',
    '<' : '>',
}

CORRUPT_SCORE_TABLE = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

INCOMPLETE_SCORE_TABLE = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}


def count_corrupted(seqs: list) -> int:
    score = 0
    for seq in seqs:
        character_stack = []
        for char in seq:
            if char in '([{<':
                character_stack.append(char)
                continue
        
            top = character_stack.pop()
            if MATCH_TABLE[top] != char:
                score += CORRUPT_SCORE_TABLE[char]
                break
    return score

def count_incomplete(seqs: list) -> int:
    from functools import reduce
    from statistics import median
    scores = []
    f = lambda p, x: 5*p + INCOMPLETE_SCORE_TABLE[MATCH_TABLE[x]]

    for seq in seqs:
        character_stack = []

        is_corrupted = False
        for char in seq:
            if char in '([{<':
                character_stack.append(char)
                continue
        
            top = character_stack.pop()
            if MATCH_TABLE[top] != char:
                is_corrupted = True
                break
        if is_corrupted: continue

        score = reduce(f, reversed(character_stack), 0)
        scores.append(score)
    return median(scores)

def get_sequences(filename: str) -> list:
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]

def main():
    sequences = get_sequences('input.txt')
    corrupted_score = count_corrupted(sequences)
    print('Part One:', corrupted_score)

    incomplete_score = count_incomplete(sequences)
    print('Part Two:', incomplete_score)

if __name__ == '__main__':
    main()