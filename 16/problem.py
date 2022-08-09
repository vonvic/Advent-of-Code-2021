"""Advent of Code 2021 Problem 16 Code Solution."""

from __future__ import annotations

from typing import Any


class _Packet:
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
    _TYPE_ID_START, _TYPE_ID_END = (
        _VERSION_END,
        _VERSION_END + _TYPE_ID_BIT_LENGTH,
    )
    _CONTENT_START = _TYPE_ID_END

    def __init__(self, bit_string: str):
        self._version: int = _Packet._get_version(bit_string)
        self._type_id: int = _Packet._get_type_id(bit_string)
        self._content_unbounded: str = _Packet._get_content_unbounded(
            bit_string
        )
        self._subpackets: list[_Packet] = []

        # initial length
        self._length = (
            _Packet._VERSION_BIT_LENGTH + _Packet._TYPE_ID_BIT_LENGTH
        )
        if self._type_id == _Packet._LITERAL_TYPE_ID:
            self._process_literal()
        else:
            # collect all subpackets first before calculating the value
            self._length_type_id = int(self._content_unbounded[0])
            if self._length_type_id == _Packet._LENGTH_OPERATOR_LENGTH_TYPE_ID:
                self._collect_subpackets_length_operator()
            else:
                self._collect_subpackets_number_operator()

            # calculate all the values
            match self._type_id:
                case 0:
                    self._process_sum()
                case 1:
                    self._process_product()
                case 2:
                    self._process_min()
                case 3:
                    self._process_max()
                case 5:
                    self._process_gt()
                case 6:
                    self._process_lt()
                case 7:
                    self._process_eq()

    def _get_version(s: str) -> int:
        return int(
            s[_Packet._VERSION_START : _Packet._VERSION_END], 2  # noqa E203
        )

    def _get_type_id(s: str) -> int:
        return int(
            s[_Packet._TYPE_ID_START : _Packet._TYPE_ID_END], 2  # noqa E203
        )

    def _get_content_unbounded(s: str) -> str:
        return s[_Packet._CONTENT_START :]  # noqa E203

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
        self._value = int(
            self._subpackets[0].value > self._subpackets[1].value
        )

    def _process_lt(self):
        self._value = int(
            self._subpackets[0].value < self._subpackets[1].value
        )

    def _process_eq(self):
        self._value = int(
            self._subpackets[0].value == self._subpackets[1].value
        )

    def _process_literal(self):
        """
        Return the literal decoded from `self._content_unbounded`.

        Loops through 5-bit sections of `self._content_unbounded. If the
        first bit of a section is not zero, then add the rest of the section
        to the resulting bit string. If it is zero, then after adding the rest
        of the section, terminate. Convert the collected bit string into a
        decimal number and set it to the value. Track the length as well.
        """
        bit_str = ""
        bit_section_length = 5
        curr = self._content_unbounded
        while curr[0] != "0":
            bit_str += curr[1:bit_section_length]
            curr = curr[bit_section_length:]
            self._length += bit_section_length
        bit_str += curr[1:bit_section_length]
        self._length += bit_section_length

        self._value = int(bit_str, 2)

    def _collect_subpackets_length_operator(self):
        """
        Collect all subpackets from a length operator.

        Collect all subpackets collectively from self._content_bounded by
        determining the length of its subpackets from bits 1 to 16. Then
        obtain and store each subpacket until the length of all the subpackets
        are equal to the length calculated beforehand.
        """
        start = 1
        end = 1 + _Packet._LENGTH_OPERATOR_VALUE_BIT_LENGTH
        self._length_of_subpackets = int(self._content_unbounded[start:end], 2)
        self._length += 1 + _Packet._LENGTH_OPERATOR_VALUE_BIT_LENGTH

        curr_length = 0
        offset = (
            _Packet._LENGTH_TYPE_BIT_LENGTH
            + _Packet._LENGTH_OPERATOR_VALUE_BIT_LENGTH
        )
        while curr_length < self._length_of_subpackets:
            subpacket = _Packet(self._content_unbounded[offset:])
            offset += subpacket.length
            curr_length += subpacket.length
            self._length += subpacket.length
            self._subpackets.append(subpacket)

    def _collect_subpackets_number_operator(self):
        """
        Collect all subpackets from a number operator.

        This is done from self._content_bounded by determining the count of its
        subpackets from bits 1 to 11. Then obtain and store each subpacket
        until the calculated number of the subpackets have been obtained.
        """
        start = 1
        end = 1 + _Packet._NUMBER_OPERATOR_VALUE_BIT_LENGTH
        self._number_of_subpackets = int(self._content_unbounded[start:end], 2)
        self._length += 1 + _Packet._NUMBER_OPERATOR_VALUE_BIT_LENGTH

        offset = (
            _Packet._LENGTH_TYPE_BIT_LENGTH
            + _Packet._NUMBER_OPERATOR_VALUE_BIT_LENGTH
        )
        for _ in range(self._number_of_subpackets):
            subpacket = _Packet(self._content_unbounded[offset:])
            offset += subpacket.length
            self._length += subpacket.length
            self._subpackets.append(subpacket)

    @property
    def version(self):
        return self._version

    @property
    def type_id(self):
        return self._type_id

    @property
    def length(self):
        return self._length

    @property
    def subpackets(self):
        return self._subpackets

    @property
    def value(self):
        return self._value

    def __str__(self):
        """Return all the information of the packet."""
        s = "Packet(\n"
        s += f"  version: {self._version}\n"
        s += f"  type ID: {self._type_id}\n"
        s += f"  length: {self._length}\n"
        s += f"  number of subpackets: {len(self._subpackets)}\n"
        s += f"  value: {self._value}\n"
        if self.type_id != _Packet._LITERAL_TYPE_ID:
            s += f"  length type ID: {self._length_type_id}\n"
            if self._length_type_id == 0:
                subpacket_length = self._length_of_subpackets
                s += f"  bit length of subpackets: {subpacket_length}\n"
            else:
                s += f"  number of subpackets: {self._number_of_subpackets}\n"
        s += ")"
        return s

    def __repr__(self):
        return str(self)


__BINARY_T0_CHAR_TABLE = {
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
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}


def __convert_string_to_bit_string(s: str):
    """
    Return the conversion of `s` into a bit string.

    The key to this function is its use of `__BINARY_T0_CHAR_TABLE`, which
    converts a character to a binary string.
    """
    from functools import reduce

    return reduce(lambda p, x: p + __BINARY_T0_CHAR_TABLE[x], s, "")


def __get_string(filename: str):
    """Return just the first line of `filename."""
    with open(filename, "r") as f:
        return f.readline()


def __version_sum(packet: _Packet) -> int:
    """
    Calculate the version sum of packet.

    The version sum is calculated by adding the version of `packet` to the
    version sums of the subpackets of `packet`.
    """
    from functools import reduce

    if len(packet.subpackets) == 0:
        return packet.version

    return reduce(
        lambda p, x: p + __version_sum(x), packet.subpackets, packet.version
    )


def part_one_answer() -> Any:
    """Return part one answer."""
    return __version_sum(__p)


def part_two_answer() -> int:
    """Return part two answer."""
    return __p.value


__string = __get_string("16/input.txt")
__bit_string = __convert_string_to_bit_string(__string)
__p = _Packet(__bit_string)
