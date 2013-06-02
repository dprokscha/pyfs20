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

from datetime import datetime
from math import log
from math import floor


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
    int_value = 0;
    for str_value in str(part):
        int_value <<= 2
        int_value += int(str_value) - 1
    return chr(int_value)

def address_to_byte(address):
    """
    Converts an address to a byte string.

    Args:
        address: String which represents a fully qualified address.

    Returns:
        >>> address_to_byte('1111-1111-4444')
        '\x00\x00\xff'

    Raises:
        InvalidInput: If the given address is invalid.
    """
    address = str(address).split('-')
    if (3 == len(address)                 and
        is_valid_address_part(address[0]) and
        is_valid_address_part(address[1]) and
        is_valid_address_part(address[2])):
        return ( address_part_to_byte(address[0])
               + address_part_to_byte(address[1])
               + address_part_to_byte(address[2])
               )
    raise InvalidInput('Invalid address given (e.g. "1234-1234-1234" expected).')

def byte_to_address(value):
    """
    Converts a byte string to an address.

    Args:
        value: Byte string.

    Returns:
        >>> byte_to_address('\x00\x00\xff')
        '1111-1111-4444'

    Raises:
        InvalidInput: If the given value is invalid.
    """
    if 3 == len(str(value)):
        return '%s-%s-%s' % (byte_to_address_part(value[0]),
                             byte_to_address_part(value[1]),
                             byte_to_address_part(value[2]))
    raise InvalidInput('Invalid address given (3 bytes expected).')

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
    address_part = ''
    for i in [3, 2, 1, 0]:
        address_part += str(((ord(value) >> i * 2) & 0x03) + 1)
    return address_part

def byte_to_time_string(value):
    """
    Converts a byte string to a time string (%H:%M:%S.%f).

    Args:
        value: Byte string.

    Returns:
        >>> byte_to_time_string('\x01')
        '00:00:0.250'
        >>> byte_to_time_string('\xcf')
        '04:16:0.000'
    """
    seconds = 2**(ord(value) >> 4) * (ord(value) & 0x0f) * 0.25
    hours = seconds / 3600
    seconds %= 3600
    minutes = seconds / 60
    seconds %= 60
    return '%02i:%02i:%.3f' % (hours, minutes, seconds)

def datetime_to_seconds(datetime):
    """
    Converts a datetime object to a value of seconds which is compatible with FS20.

    Args:
        datetime: Python datetime object.

    Returns:
        >>> datetime_to_seconds(datetime.strptime('01:20:12.350', '%H:%M:%S.%f'))
        4812.250
    """
    seconds = ( datetime.hour   * 3600
              + datetime.minute * 60
              + datetime.second
              + float(datetime.microsecond) / 10**6
              )
    offset = 0.25 - (seconds % 0.25)
    if 0.25 == offset:
        offset = 0
    if 0.125 > offset or 0.250 > seconds:
        seconds += offset
    else:
        seconds -= seconds % 0.25
    return seconds

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

def time_string_to_byte(time_string):
    """
    Converts a time string to a byte string.

    Args:
        time_string: A time string like "%H:%M:%S.%f" (between 0ms and 4h 16m).

    Returns:
        >>> time_string_to_byte('00:01:4.0')
        '\x58'
        >>> time_string_to_byte('04:16:0.0')
        '\xcf'
    """
    seconds = datetime_to_seconds(datetime.strptime(time_string, '%H:%M:%S.%f'))
    if 0.0 == seconds:
        return '\x00'
    if not seconds <= 15360.0:
        raise InvalidInput('Only times between 0ms and 4h 16m are supported.')
    high_nibble = int(floor(log(seconds, 2))) - 1
    if 0 > high_nibble:
        high_nibble = 0
    low_nibble = int(seconds / (2**high_nibble * 0.25))
    return chr((high_nibble << 4) + low_nibble)


class InvalidInput(Exception):
    pass