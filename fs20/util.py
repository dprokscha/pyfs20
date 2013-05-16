# -*- coding: utf-8 -*-

# Copyright (c) 2013 Daniel Prokscha
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

def address_part_to_byte(part):
    """
    Converts an address part to a byte string.

    Args:
        part: String or integer which represents an address part.

    Returns:
        >>> address_part_to_byte(1111)
        '\x00'
        >>> address_part_to_byte('4444')
        '\xff'
    """
    return chr(address_part_to_int(part))

def address_part_to_hex(part):
    """
    Converts an address part to it's hexadecimal value.

    Args:
        part: String or integer which represents an address part.

    Returns:
        >>> address_part_to_hex(1111)
        0x0
        >>> address_part_to_hex('4444')
        0xff
    """
    return hex(address_part_to_int(part))

def address_part_to_int(part):
    """
    Converts an address part to it's integer value.

    Args:
        part: String or integer which represents an address part.

    Returns:
        >>> address_part_to_int(1111)
        0x0
        >>> address_part_to_int('4444')
        0xff
    """
    int_value = 0;
    for key_code in str(part):
        int_value <<= 2
        int_value += int(key_code) - 1
    return int_value

def byte_to_address_part(value):
    """
    Converts a byte string to an address part.

    Args:
        value: Byte string.

    Returns:
        >>> byte_to_address_part('\x00')
        '1111'
        >>> byte_to_address_part('\xff')
        '4444'
    """
    return int_to_address_part(ord(value))

def hex_to_address_part(value):
    """
    Converts a hexadecimal value to an address part.

    Args:
        value: Hexadecimal value.

    Returns:
        >>> hex_to_address_part(0x0)
        '1111'
        >>> hex_to_address_part(0xff)
        '4444'
    """
    return int_to_address_part(int(value))

def int_to_address_part(value):
    """
    Converts an integer value to an address part.

    Args:
        value: Integer value.

    Returns:
        >>> int_to_address_part(0)
        '1111'
        >>> int_to_address_part(255)
        '4444'
    """
    address_part = ''
    for i in range(3, -1, -1):
        address_part += str(((value >> i * 2) & 0x03) + 1)
    return address_part

def is_valid_address_part(part):
    """
    Returns TRUE if the given address part is a valid FS20 address part.

    Args:
        part: String or integer which represents an address part.

    Returns:
        >>> is_valid_address_part('1112')
        True
        >>> is_valid_address_part(4448)
        False
    """
    if 4 == len(str(part)):
        for i in str(part):
            if not 1 <= int(i) <= 4:
                return False
        return True
    return False


class InvalidInput(Exception):
    pass