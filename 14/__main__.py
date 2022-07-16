import enum
from typing import Callable

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

# def run_pair_insertion(template: str, rules: dict) -> str:
#     new_polymer = ''
#     for i in range(len(template)-1):
#         new_polymer += template[i] + rules[template[i:i+2]]
#     return new_polymer + template[-1]

# _OPT_SAVED = dict()
# def _OPT(A: str, B: str, rules: dict, N: int) -> str:
#     key = (A, B, N)
#     if key in _OPT_SAVED: return _OPT_SAVED[key]
#     if N == 0: return ''

#     M: str = rules[A+B]
#     s = _OPT(A, M, rules, N-1) + M + _OPT(M, B, rules, N-1)
#     _OPT_SAVED[key] = s
#     return s

# def run_pair_insertion_N_times(template: str, rules: dict, N: int) -> str:
#     polymer = ''

#     for i in range(len(template)-1):
#         print(i)
#         A, B = template[i], template[i+1]
#         polymer += A + _OPT(A, B, rules, N)
#     print('complete')
#     return polymer + template[-1]

def get_frequency_table(s: str) -> dict:
    freq_table = dict()
    for c in s:
        freq_table[c] = freq_table.get(c, 0) + 1
    return freq_table

# def get_part_one_answer(template: str, rules: dict, N: int) -> int:
#     s = run_pair_insertion_N_times(template, rules, N)
#     f = get_frequency_table(s)
#     max_freq, min_freq = f[max(f, key=f.get)], f[min(f, key=f.get)]
#     return max_freq - min_freq

_OPT_SAVED: dict[tuple[str, str, int], Callable] = dict()
def _OPT(A: str, B: str, rules: dict, N: int, freq: dict) -> str:
    if N == 0: return ''

    key = (A, B, N)
    if key in _OPT_SAVED:
        _OPT_SAVED[key]()
        return

    def f():
        M: str = rules[A+B]
        freq[M] = freq.get(M, 0) + 1
        _OPT(A, M, rules, N-1, freq)
        _OPT(M, B, rules, N-1, freq)
        print
    
    _OPT_SAVED[key] = f
    f()

_OPT2_SAVED = dict()
def _OPT2(A: str, B: str, rules: dict, N: int) -> str:
    if N == 0: return ''
    key = (A, B, N)
    if key in _OPT2_SAVED: return _OPT2_SAVED[key]

    M = rules[A+B]
    L_key = (A, M, N-1)
    L = _OPT2_SAVED[L_key] if L_key in _OPT2_SAVED else _OPT2(A, M, rules, N-1)
    R_key = (M, B, N-1)
    R = _OPT2_SAVED[R_key] if R_key in _OPT2_SAVED else _OPT2(M, B, rules, N-1)
    s = L + M + R
    _OPT2_SAVED[key] = s
    return s

def get_most_and_least_freq_diff(template: str, rules: dict, N: int) -> int:
    freq = dict()
    for i, value in enumerate(template[:-1]):
        A, B = value, template[i+1]
        freq[A] = freq.get(A, 0) + 1
        _OPT(A, B, rules, N, freq)
    last = template[-1]
    freq[last] = freq.get(last, 0) + 1
    most, least = max(freq, key=freq.get), min(freq, key=freq.get)
    return freq[most] - freq[least]

def main():
    template, rules = get_template_and_rules('sample.txt')
    N = 40
    # part_one_s = _OPT2('N', 'N', rules, N)
    # print('complete')
    # part_one = get_most_and_least_freq_diff(template, rules, N)
    # N = 40
    # part_two = get_most_and_least_freq_diff(template, rules, N)

    # print(part_one)
    # print(part_two)

if __name__ == '__main__':
    main()