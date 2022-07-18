from __future__ import annotations
from lib2to3.pgen2.grammar import opmap_raw

class Packet:
    _VERSION_BIT_LENGTH: int = 3
    _TYPE_ID_BIT_LENGTH: int = 3
    _LENGTH_TYPE_BIT_LENGTH: int = 1
    _NUMBER_OPERATOR_VALUE_BIT_LENGTH = 11
    _LENGTH_OPERATOR_VALUE_BIT_LENGTH = 15

    _LITERAL_TYPE_ID = 4
    _LENGTH_OPERATOR_LENGTH_TYPE_ID = 0
    _NUMBER_OPERATOR_LENGTH_TYPE_ID = 1
    def __init__(self, bit_string: str):
        version_start, version_end = 0, Packet._VERSION_BIT_LENGTH
        type_id_start, type_id_end = version_end, version_end + Packet._TYPE_ID_BIT_LENGTH
        content_start = type_id_end
        number_base = 2
        self._version: int = int(bit_string[version_start:version_end], number_base)
        self._type_id: int = int(bit_string[type_id_start:type_id_end], number_base)
        self._content_unbounded: str = bit_string[content_start:]
        self._subpackets = []

        self._length = Packet._VERSION_BIT_LENGTH + Packet._TYPE_ID_BIT_LENGTH
        if self._type_id == Packet._LITERAL_TYPE_ID:
            self.process_literal()
        else:
            self._length_type_id = int(self._content_unbounded[0])
            if self._length_type_id == Packet._LENGTH_OPERATOR_LENGTH_TYPE_ID:
                self.process_length_operator()
            else:
                self.process_number_operator()

    def process_literal(self):
        bit_str = ''
        bit_section_length = 5
        curr = self._content_unbounded
        while curr[0] != '0':
            bit_str += curr[1:bit_section_length]
            curr = curr[bit_section_length:]
            self._length += bit_section_length
        bit_str += curr[1:bit_section_length]
        self._length += bit_section_length

        self._literal_value = int(bit_str, 2)
    def process_length_operator(self):
        start = 1
        end = 1 + Packet._LENGTH_OPERATOR_VALUE_BIT_LENGTH
        self._length_of_subpackets = int(self._content_unbounded[start:end], 2)
        self._length += 1 + Packet._LENGTH_OPERATOR_VALUE_BIT_LENGTH

        curr_length = 0
        offset = Packet._LENGTH_TYPE_BIT_LENGTH + Packet._LENGTH_OPERATOR_VALUE_BIT_LENGTH
        while curr_length < self._length_of_subpackets:
            subpacket = Packet(self._content_unbounded[offset:])
            offset += subpacket.length
            curr_length += subpacket.length
            self._length += subpacket.length
            self._subpackets.append(subpacket)
        
    def process_number_operator(self):
        start = 1
        end = 1 + Packet._NUMBER_OPERATOR_VALUE_BIT_LENGTH
        self._number_of_subpackets = int(self._content_unbounded[start:end], 2)
        self._length += 1 + Packet._NUMBER_OPERATOR_VALUE_BIT_LENGTH

        offset = Packet._LENGTH_TYPE_BIT_LENGTH + Packet._NUMBER_OPERATOR_VALUE_BIT_LENGTH
        for _ in range(self._number_of_subpackets):
            subpacket = Packet(self._content_unbounded[offset:])
            offset += subpacket.length
            self._length += subpacket.length
            self._subpackets.append(subpacket)

    @property
    def version(self): return self._version

    @property
    def type_id(self): return self._type_id

    @property
    def length(self): return self._length

    @property
    def subpackets(self): return self._subpackets

    def __str__(self):
        s = 'Packet(\n'
        s += f'  version: {self._version}\n'
        s += f'  type ID: {self._type_id}\n'
        s += f'  length: {self._length}\n'
        s += f'  number of subpackets: {len(self._subpackets)}\n'
        if self.type_id == Packet._LITERAL_TYPE_ID:
            s += f'  literal value: {self._literal_value}\n'
        else:
            s += f'  length type ID: {self._length_type_id}\n'
            if self._length_type_id == 0:
                s += f'  bit length of subpackets: {self._length_of_subpackets}\n'
            else:
                s += f'  number of subpackets: {self._number_of_subpackets}\n'
        s += ')'
        return s
    def __repr__(self): return str(self)

BINARY_T0_CHAR_TABLE = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    'A': "1010",
    'B': "1011",
    'C': "1100",
    'D': "1101",
    'E': "1110",
    'F': "1111"
}

def convert_string_to_bit_string(s: str):
    from functools import reduce
    return reduce(lambda p, x: p+BINARY_T0_CHAR_TABLE[x], s, '')

def get_string(filename: str):
    with open(filename, 'r') as f: return f.readline()

def version_sum(packet: Packet) -> int:
    from functools import reduce
    if len(packet.subpackets) == 0:
        return packet.version

    current_sum = packet.version
    for subpacket in packet.subpackets:
        current_sum += version_sum(subpacket)
    return current_sum

def main():
    string = get_string('input.txt')
    print('String:', string)
    bit_string = convert_string_to_bit_string(string)
    p = Packet(bit_string)
    print('Length:', p.length)
    print('Subpackets:', p.subpackets)

    print('Version sum:', version_sum(p))

if __name__ == '__main__':
    main()