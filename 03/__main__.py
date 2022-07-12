import re

def gamma_and_epsilon(diagnostics: list) -> tuple:
    gamma: str
    epsilon: str

    bits = [0 for _ in range(len(diagnostics[0]))]

    for diagnostic in diagnostics:
        for i, bit in enumerate(diagnostic):
            bits[i] += 1 if bit == '1' else -1

    gamma = ''.join(map(lambda x: '1' if x > 0 else '0', bits))
    epsilon = ''.join(map(lambda x: '0' if x > 0 else '1', bits))

    return (gamma, epsilon)

def get_oxygen_generator(diagnostics: list) -> int:
    count = [0 for _ in range(len(diagnostics[0]))]

    s = ''
    for i in range(len(count)):
        matched_count, matched_s = 0, ''
        for diagnostic in diagnostics:
            if re.match(s, diagnostic):
                matched_count += 1
                matched_s = diagnostic
                count[i] += 1 if diagnostic[i] == '1' else -1
        if matched_count == 1:
            s = matched_s
            break
        s += '1' if count[i] >= 0 else '0'
    
    return s

def get_co2_scrubber(diagnostics: list) -> int:
    count = [0 for _ in range(len(diagnostics[0]))]

    s = ''
    for i in range(len(count)):
        matched_count, matched_s = 0, ''
        for diagnostic in diagnostics:
            if re.match(s, diagnostic):
                matched_count += 1
                matched_s = diagnostic
                count[i] += 1 if diagnostic[i] == '1' else -1
        if matched_count == 1:
            s = matched_s
            break
        s += '0' if count[i] >= 0 else '1'
    
    return s

if __name__ == '__main__':
    diagnostics: list
    with open('input.txt', 'r') as f:
        diagnostics = [x.strip() for x in f.readlines()]
    gamma, epsilon = gamma_and_epsilon(diagnostics)
    gamma_int, epsilon_int = int(gamma, 2), int(epsilon, 2)
    oxygen_generator = get_oxygen_generator(diagnostics)
    oxygen_generator_int = int(oxygen_generator, 2)
    co2_scrubber = get_co2_scrubber(diagnostics)
    co2_scrubber_int = int(co2_scrubber, 2)
    print(f'Gamma: {gamma_int}')
    print(f'Epsilon: {epsilon_int}')
    print(f'Multiplied: {gamma_int*epsilon_int}')
    print(f'Oxygen Generator Rating: {oxygen_generator_int}')
    print(f'CO2 Scrubber Rating: {co2_scrubber_int}')
    print(f'Life Support Rating: {oxygen_generator_int * co2_scrubber_int}')