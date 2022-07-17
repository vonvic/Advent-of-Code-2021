from collections import namedtuple
from typing import Type

class Packet:
    def __init__(self, bit_string):
        self._version: int = int(bit_string[:3], 2)
        self._type_id: int = int(bit_string[3:6], 2)
        self._content: str = bit_string[6:]
        
        self._literal_value = None
        self._length_type_id = None
        self._length_of_subpackets = None
        self._number_of_subpackets = None

        if self.is_literal_packet:
            self._literal_value = self.calc_literal_value()
        else:
            self._length_type_id = int(self._content[0], 2)
            if self._length_type_id == 0:
                bit_length = 15
                self._length_of_subpackets = int(self._content[1:1+bit_length], 2)

                self.rtrim_at(1+bit_length+self._length_of_subpackets)
            else:
                bit_length = 11
                self._number_of_subpackets = int(self._content[1:1+bit_length], 2)
    
    @property
    def version(self): return self._version

    @property
    def type_id(self): return self._type_id

    @property
    def content(self): return self._content

    @property
    def is_literal_packet(self): return self._type_id == 4

    @property
    def is_operator_packet(self): return self.type_id != 4

    @property
    def length_type_id(self): return self._length_type_id

    @property
    def is_length_operator_packet(self): return self.length_type_id == 0

    @property
    def is_number_operator_packet(self): return self.length_type_id == 1

    @property
    def length_of_subpackets(self): return self._length_of_subpackets

    @property
    def number_of_subpackets(self): return self._number_of_subpackets

    @property
    def literal_value(self): return self._literal_value

    def calc_literal_value(self):
        bit_string = ''

        s = self._content

        while s[0] != '0':
            bit_string += s[1:5]
            s = s[5:]
        bit_string += s[1:5]

        return int(bit_string, 2)

    def rtrim_at(self, index): self._content[:index]

    def __str__(self):
        s = 'Packet(\n'
        s += f'  version: {self._version}\n'
        s += f'  type ID: {self._type_id}\n'
        if self.is_operator_packet:
            s += f'  length type ID: {self._length_type_id}\n'
            if self._length_type_id == 0:
                s += f'  bit length of subpackets: {self.get_length_of_subpackets}\n'
            else:
                s += f'  number of subpackets: {self.get_number_of_subpackets}\n'
        else:
            s += f'  literal value: {self._literal_value}\n'
        s += ')'
        return s

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

def process_literal(s: str) -> int:
    bit_string = ''

    while s[0] != '0':
        bit_string += s[1:5]
        s = s[5:]
    bit_string += s[1:5]

    return int(bit_string, 2)

def get_string(filename: str):
    with open(filename, 'r') as f: return f.readline()

def get_next_packet(bit_string: str) -> tuple[Packet, str]:
    

def get_all_packets(bit_string: str):
    packet = Packet(bit_string)
    if packet.is_literal_packet:
        return len(bit_string), {packet}
    
    if packet.is_length_operator_packet:
        subpackets = set()
        current_length = 0
        while current_length < packet.length_of_subpackets:
            subpacket_length, subpackets_subpackets = get_all_packets()
def main():
    string = get_string('sample2.txt')
    bit_string = convert_string_to_bit_string(string)
    get_all_packets(bit_string)

if __name__ == '__main__':
    main()