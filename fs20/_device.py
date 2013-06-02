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

from functools import partial

from fs20 import pcs
from fs20 import util


class Device:
    """
    Abstract class for device abstraction layers.

    Attributes:
        address: A string which represents a fully qualified address.
        callables: A dictionary which holds all callable commands of the device.
        blocked: Is set to TRUE it the device is blocked.
        status: Holds the current device status (brightness level 0-100 or "None" for unknown).
    """

    callables = {}

    def __getattr__(self, name):
        """
        Returns a callable for the given command name.

        Args:
            name: String which represents the command name.

        Returns:
            >>> self.command_name()
            <type 'instancemethod'>

        Raises:
            UnknownCommand: If the given command name does not exists.
        """
        if name in self.callables:
            return partial( self.callable
                          , command=self.callables[name]['command']
                          , status=self.callables[name]['status']
                          )
        raise UnknownCommand('Command "%s" does not exists.' % (name))

    def __init__(self, address = '1111-1111-1111'):
        """
        Initializes device instance.

        Args:
            address: A string which represents a fully qualified address (defaults to "1111-1111-1111").
        """
        self._pcs = pcs.PCS()
        self.address = util.address_to_byte(address)
        self.blocked = False
        self.status = 0

    def callable(self, command='\x00', status=None, time_string='00:00:0.0', interval=1):
        """
        Executes the command and returns the new device status on success.

        Args:
            command: Byte string which represents a fully qualified command.
            status: The new device status (brightness level 0-100 or "None" for unknown).
            time_string: A time string like "%H:%M:%S.%f" (between 0ms and 4h 16m).
            interval: Interval between 1 and 255 how often the command should be sent.

        Returns:
            >>> self.callable('\x00', 75)
            75

        Raises:
            DeviceBlocked: If the device is currently blocked.
        """
        if self.blocked:
            raise DeviceBlocked('Device is currently blocked.')
        if interval is 1:
            response = self._pcs.send_once( address=self.address
                                          , command=command
                                          , time=util.time_string_to_byte(time_string)
                                          )
        else:
            response = self._pcs.send_multiple( address=self.address
                                              , command=command
                                              , time=util.time_string_to_byte(time_string)
                                              , interval=interval
                                              )
        if pcs.RESPONSE_OK == response:
            self.status = status
        return self.status


class DeviceBlocked(Exception):
    pass


class UnknownCommand(Exception):
    pass