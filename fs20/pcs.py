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

from array import array

import usb

# USB device ID of FS20 PCS.
ID_PRODUCT = 0xe015
ID_VENDOR = 0x18ef

# I/O endpoints.
ENDPOINT_READ = 0x81
ENDPOINT_WRITE = 0x01

# Possible data frames.
DATAFRAME_SEND_ONCE = '\x01\x06\xf1'
DATAFRAME_SEND_MULTIPLE = '\x01\x07\xf2'
DATAFRAME_STOP_MULTIPLE_SENDING = '\x01\x01\xf3'
DATAFRAME_VERSION = '\x01\x01\xf0'

# Possible response codes.
RESPONSE_DATAFRAME_UNKNOWN = 0x02
RESPONSE_DATAFRAME_MISMATCH = 0x03
RESPONSE_FIRMWARE_REQUEST_OK = 0x01
RESPONSE_OK = 0x00
RESPONSE_STOP_MULTIPLE_SENDING_OK = 0x04
RESPONSE_STOP_MULTIPLE_SENDING_NOT_SENT = 0x05


class PCS:
    """
    Handles I/O of FS20 PCS.
    """

    def _get_device(self):
        """
        Returns FS20 PCS device instance.

        Returns:
            >>> self._get_device()
            <usb.core.Device object>

        Raises:
            DeviceNotFound: If FS20 PCS is not connected or can't be found.
        """
        device = usb.core.find(idVendor=ID_VENDOR,
                               idProduct=ID_PRODUCT)
        if device is None:
            raise DeviceNotFound('FS20 PCS not found.')
        # Set configuration if there is no active one.
        try:
            device.get_active_configuration()
        except Exception:
            device.set_configuration()
        # Force I/O if device seems to be busy.
        try:
            device.detach_kernel_driver(0)
        except Exception:
            pass
        return device

    def _get_raw_address(self, address):
        """
        Returns a raw address.

        Args:
            address: Byte string which represents a fully qualified address.

        Returns:
            >>> self._get_raw_address('\xff\xff\xff')
            '\xff\xff\xff'

        Raises:
            InvalidInput: If more or less then 3 bytes given.
        """
        if 3 == len(address):
            return address
        raise InvalidInput('Invalid address given (3 bytes expected).')

    def _get_raw_command(self, command):
        """
        Returns a raw command, which is always two bytes long.

        Args:
            command: Byte string which represents a fully qualified command.

        Returns:
            >>> self._get_raw_address('\x00\x00')
            '\x00\x00'
            >>> self._get_raw_address('\x01')
            '\x01\x00'

        Raises:
            InvalidInput: If more then two or less then one bytes given.
        """
        if 2 == len(command):
            return command
        elif 1 == len(command):
            return command + '\x00'
        raise InvalidInput('Invalid command given (1-2 bytes expected).')

    def _get_raw_interval(self, interval):
        """
        Returns a raw interval.

        Args:
            interval: Integer value which represents an interval.

        Returns:
            >>> self._get_raw_interval(15)
            '\x0f'

        Raises:
            InvalidInput: If the given interval is not between 1 and 255.
        """
        if 1 <= int(interval) <= 255:
            return chr(int(interval))
        raise InvalidInput('Invalid interval given (1-255 expected).')

    def _get_response(self):
        """
        Returns the response of PCS FS20 (after sending commands).

        Returns:
            >>> self._get_response()
            '\x00\x00'
            >>> self._get_response()
            '\x01\x10'

        Raises:
            DeviceCommandUnknown: If an unknown command was sent to FS20 PCS.
            DeviceCommandMismatch: If FS20 PCS can't handle the sent command.
            DeviceInvalidResponse: If FS20 PCS returns an invalid response.
        """
        try:
            response = self._get_device().read(ENDPOINT_READ, 5, timeout=500)
        except Exception:
            response = ''
        if response[0:3] == array('B', [0x02, 0x03, 0xa0]):
            if response[3] in [RESPONSE_STOP_MULTIPLE_SENDING_OK,
                               RESPONSE_STOP_MULTIPLE_SENDING_NOT_SENT,
                               RESPONSE_FIRMWARE_REQUEST_OK,
                               RESPONSE_OK]:
                return response[3:5]
            elif RESPONSE_DATAFRAME_UNKNOWN == response[3]:
                raise DeviceDataframeUnknown('Unknown data frame sent to device.')
            elif RESPONSE_DATAFRAME_MISMATCH == response[3]:
                raise DeviceDataframeMismatch('Device can not handle data frame.')
        raise DeviceInvalidResponse('Invalid response from device.')

    def _write(self, dataframe, with_response=True):
        """
        Writes the given data frame to FS20 PCS.

        Args:
            dataframe: Byte string which represents a fully qualified data frame.
            with_response: Boolean value whether to get a response from the sent command.

        Returns:
            Depends from the given data frame.
        """
        self._get_device().write(ENDPOINT_WRITE, dataframe)
        if with_response:
            return self._get_response()
        return array('B', [RESPONSE_OK, 0])

    def get_version(self):
        """
        Returns the firmware version of FS20 PCS.

        Returns:
            >>> self.get_version()
            'v1.7'
        """
        version = str(self._write(DATAFRAME_VERSION)[1])
        return 'v%s.%s' % (version[0], version[1])

    def send_multiple(self, address, command, time='\x00', interval=1):
        """
        Sends the given command multiple for the given address.

        Args:
            address: Byte string which represents a fully qualified address.
            command: Byte string which represents a fully qualified command.
            time: Byte string which represents a fully qualified time.
            interval: Interval between 1 and 255 how often the command should be sent.

        Returns:
            >>> self.send_multiple('\x00\x00\x00', '\x10', 10)
            '\x00'
        """
        return self._write( DATAFRAME_SEND_MULTIPLE
                          + self._get_raw_address(address)
                          + self._get_raw_command(command + time)
                          + self._get_raw_interval(interval)
                          , False
                          )[0]

    def send_once(self, address, command, time='\x00'):
        """
        Sends the given command once for the given address.

        Args:
            address: Byte string which represents a fully qualified address.
            command: Byte string which represents a fully qualified command.
            time: Byte string which represents a fully qualified time.

        Returns:
            >>> self.send('\x00\x00\x00', '\x10')
            '\x00'
        """
        return self._write( DATAFRAME_SEND_ONCE
                          + self._get_raw_address(address)
                          + self._get_raw_command(command + time)
                          )[0]

    def stop_multiple_sending(self):
        """
        Stops instantly the multiple sending of a command.

        Returns:
            >>> self.stop_multiple_sending()
            '\x04'
        """
        return self._write(DATAFRAME_STOP_MULTIPLE_SENDING)[0]


# Module exceptions.
class DeviceDataframeMismatch(Exception):
    pass


class DeviceDataframeUnknown(Exception):
    pass


class DeviceInvalidResponse(Exception):
    pass


class DeviceNotFound(Exception):
    pass


class InvalidInput(Exception):
    pass