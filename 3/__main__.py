from numpy import diag


def gamma_and_epsilon(diagnostics: list) -> tuple:
    gamma: int
    epsilon: int

    bits = [0 for _ in range(len(diagnostics[0]))]

    for diagnostic in diagnostics:
        for i, bit in enumerate(diagnostic):
            bits[i] += 1 if bit == '1' else -1

    gamma = ''.join(map(lambda x: '1' if x > 0 else '0', bits))
    epsilon = ''.join(map(lambda x: '0' if x > 0 else '1', bits))

    return (gamma, epsilon)

if __name__ == '__main__':
    diagnostics: list
    with open('input.txt', 'r') as f:
        diagnostics = [x.strip() for x in f.readlines()]
    gamma, epsilon = gamma_and_epsilon(diagnostics)
    gamma_int, epsilon_int = int(gamma, 2), int(epsilon, 2)
    print(f'Gamma: {gamma_int}')
    print(f'Epsilon: {epsilon_int}')
    print(f'Multiplied: {gamma_int*epsilon_int}')