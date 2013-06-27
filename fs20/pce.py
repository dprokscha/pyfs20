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
from binascii import hexlify

import usb

# USB device ID of FS20 PCE.
ID_PRODUCT = 0xe014
ID_VENDOR = 0x18ef

# I/O endpoint.
ENDPOINT_READ = 0x81


class PCE:
    """
    Handles I/O of FS20 PCE.

    Attributes:
        version: Holds the firmware version of FS20 PCE.
    """

    version = None

    def _get_device(self):
        """
        Returns FS20 PCE device instance.

        Returns:
            >>> self._get_device()
            <usb.core.Device object>

        Raises:
            DeviceNotFound: If FS20 PCE is not connected or can't be found.
        """
        device = usb.core.find(idVendor=ID_VENDOR,
                               idProduct=ID_PRODUCT)
        if device is None:
            raise DeviceNotFound('FS20 PCE not found.')
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

    def get_response(self):
        """
        Returns the response of FS20 PCE (after receiving commands).

        Returns:
            >>> self.get_response()
            <fs20.pce.Response>

        Raises:
            DeviceInvalidResponse: If FS20 PCE returns an invalid response or there is none.
        """
        try:
            response = self._get_device().read(ENDPOINT_READ, 13, timeout=100)
        except Exception:
            response = ''
        if response[0:2] == array('B', [0x02, 0x0b]):
            PCE.version = response[12]
            return Response(response[2:])
        raise DeviceInvalidResponse('Invalid response from device.')

    def get_version(self):
        """
        Returns the firmware version of FS20 PCE.

        Returns:
            >>> self.get_version()
            'v2.2'

        Raises:
            DeviceMissingResponse: If FS20 PCE has not yet received any commands.
        """
        if PCE.version is None:
            raise DeviceMissingResponse('Version only available after receiving commands.')
        version = str(PCE.version)
        return 'v%s.%s' % (version[0], version[1])


class Response:
    """
    Handles response of FS20 PCE.

    Attributes:
        address: String which represents a fully qualified address (response target).
        command: Byte string which represents a fully qualified command.
        time: Float value which represents the execution time for the command (seconds).
    """
    def __init__(self, response):
        self.address = '%s-%s-%s' % ( hexlify(response[0:2])
                                    , hexlify(response[2:4])
                                    , hexlify(response[4:6])
                                    )
        self.command = hexlify(response[6:7])
        self.time = hexlify(response[7:10])
        if 1 == int(self.time[0]):
            self.time = 0.25 * float(self.time[1:])
        else:
            self.time = 0.0

    def __str__(self):
        return 'Address: %s, Command: %s, Time: %s' % ( self.address
                                                      , self.command
                                                      , self.time
                                                      )


# Module exceptions.
class DeviceInvalidResponse(Exception):
    pass


class DeviceMissingResponse(Exception):
    pass


class DeviceNotFound(Exception):
    pass