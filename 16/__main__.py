from __future__ import annotations
from ast import Return

class Packet:
    _VERSION_BIT_LENGTH: int = 3
    _TYPE_ID_BIT_LENGTH: int = 3
    _LENGTH_TYPE_BIT_LENGTH: int = 1
    _NUMBER_OPERATOR_VALUE_BIT_LENGTH = 11
    _LENGTH_OPERATOR_VALUE_BIT_LENGTH = 15

    _SUM_TYPE_ID = 0
    _PRODUCT_TYPE_ID = 1
    _MINIMUM_TYPE_ID = 2
    _MAXIMUM_TYPE_ID = 3
    _LITERAL_TYPE_ID = 4
    _GT_TYPE_ID = 5
    _LT_TYPE_ID = 6
    _EQ_TYPE_ID = 7

    _LENGTH_OPERATOR_LENGTH_TYPE_ID = 0
    _NUMBER_OPERATOR_LENGTH_TYPE_ID = 1

    _VERSION_START, _VERSION_END = 0, _VERSION_BIT_LENGTH
    _TYPE_ID_START, _TYPE_ID_END = _VERSION_END, _VERSION_END + _TYPE_ID_BIT_LENGTH
    _CONTENT_START = _TYPE_ID_END
    def __init__(self, bit_string: str):
        self._version: int = Packet._get_version(bit_string)
        self._type_id: int = Packet._get_type_id(bit_string)
        self._content_unbounded: str = Packet._get_content_unbounded(bit_string)
        self._subpackets: list[Packet] = []

        # initial length
        self._length = Packet._VERSION_BIT_LENGTH + Packet._TYPE_ID_BIT_LENGTH
        if self._type_id == Packet._LITERAL_TYPE_ID:
            self._process_literal()
        else:
            # collect all subpackets first before calculating the value
            self._length_type_id = int(self._content_unbounded[0])
            if self._length_type_id == Packet._LENGTH_OPERATOR_LENGTH_TYPE_ID:
                self._collect_subpackets_length_operator()
            else:
                self._collect_subpackets_number_operator()

            # calculate all the values
            match self._type_id:
                case 0: self._process_sum()
                case 1: self._process_product()
                case 2: self._process_min()
                case 3: self._process_max()
                case 5: self._process_gt()
                case 6: self._process_lt()
                case 7: self._process_eq()
            
    def _get_version(s: str) -> int:
        return int(s[Packet._VERSION_START:Packet._VERSION_END], 2)
    
    def _get_type_id(s: str) -> int:
        return int(s[Packet._TYPE_ID_START:Packet._TYPE_ID_END], 2)

    def _get_content_unbounded(s: str) -> str:
        return s[Packet._CONTENT_START:]

    def _process_sum(self):
        from functools import reduce
        self._value = reduce(lambda p, x: p + x.value, self._subpackets, 0)
    
    def _process_product(self):
        from functools import reduce
        self._value = reduce(lambda p, x: p * x.value, self._subpackets, 1)

    def _process_min(self):
        self._value = min(self._subpackets, key=lambda p: p.value).value

    def _process_max(self):
        self._value = max(self._subpackets, key=lambda p: p.value).value

    def _process_gt(self):
        self._value = int(self._subpackets[0].value > self._subpackets[1].value)
    
    def _process_lt(self):
        self._value = int(self._subpackets[0].value < self._subpackets[1].value)
    
    def _process_eq(self):
        self._value = int(self._subpackets[0].value == self._subpackets[1].value)

    def _process_literal(self):
        '''Loops through 5-bit sections of `self._content_unbounded. If the
        first bit of a section is not zero, then add the rest of the section
        to the resulting bit string. If it is zero, then after adding the rest
        of the section, terminate. Convert the collected bit string into a
        decimal number and set it to the value. Track the length as well.'''
        bit_str = ''
        bit_section_length = 5
        curr = self._content_unbounded
        while curr[0] != '0':
            bit_str += curr[1:bit_section_length]
            curr = curr[bit_section_length:]
            self._length += bit_section_length
        bit_str += curr[1:bit_section_length]
        self._length += bit_section_length

        self._value = int(bit_str, 2)
    def _collect_subpackets_length_operator(self):
        '''Collect all subpackets collectively from self._content_bounded by
        determining the length of its subpackets from bits 1 to 16. Then
        obtain and store each subpacket until the length of all the subpackets
        are equal to the length calculated beforehand.'''
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
        
    def _collect_subpackets_number_operator(self):
        '''Collect all subpackets collectively from self._content_bounded by
        determining the count of its subpackets from bits 1 to 11. Then obtain
        and store each subpacket until the calculated number of the
        subpackets have been obtained.'''
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

    @property
    def value(self): return self._value

    def __str__(self):
        '''Returns all the information of the packet.'''
        s = 'Packet(\n'
        s += f'  version: {self._version}\n'
        s += f'  type ID: {self._type_id}\n'
        s += f'  length: {self._length}\n'
        s += f'  number of subpackets: {len(self._subpackets)}\n'
        s += f'  value: {self._value}\n'
        if self.type_id != Packet._LITERAL_TYPE_ID:
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

    return reduce(lambda p, x: p + version_sum(x), packet.subpackets, packet.version)

def main():
    string = get_string('input.txt')
    bit_string = convert_string_to_bit_string(string)
    p = Packet(bit_string)

    print('Version sum:', version_sum(p))
    print(p)

if __name__ == '__main__':
    main()