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

from fs20 import command
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


class Dimmer(Device):
    """
    Abstraction layer for all FS20 dimmer devices.
    """

    callables = {
        """
        Single byte commands.
        """
        'change_internal_timer': {
            'command': command.CHANGE_INTERNAL_TIMER,
            'status': None
        },
        'dim_down': {
            'command': command.DIM_DOWN,
            'status': None
        },
        'dim_up': {
            'command': command.DIM_UP,
            'status': None
        },
        'dim': {
            'command': command.DIM,
            'status': None
        },
        'educate': {
            'command': command.EDUCATE,
            'status': None
        },
        'off': {
            'command': command.OFF,
            'status': 0
        },
        'off_for_internal_time_then_last_brightness_level': {
            'command': command.OFF_FOR_INTERNAL_TIME_THEN_LAST_BRIGHTNESS_LEVEL,
            'status': None
        },
        'on': {
            'command': command.ON,
            'status': 100
        },
        'on_brightness_level_1': {
            'command': command.ON_BRIGHTNESS_LEVEL_1,
            'status': 6
        },
        'on_brightness_level_2': {
            'command': command.ON_BRIGHTNESS_LEVEL_2,
            'status': 12
        },
        'on_brightness_level_3': {
            'command': command.ON_BRIGHTNESS_LEVEL_3,
            'status': 18
        },
        'on_brightness_level_4': {
            'command': command.ON_BRIGHTNESS_LEVEL_4,
            'status': 25
        },
        'on_brightness_level_5': {
            'command': command.ON_BRIGHTNESS_LEVEL_5,
            'status': 31
        },
        'on_brightness_level_6': {
            'command': command.ON_BRIGHTNESS_LEVEL_6,
            'status': 37
        },
        'on_brightness_level_7': {
            'command': command.ON_BRIGHTNESS_LEVEL_7,
            'status': 43
        },
        'on_brightness_level_8': {
            'command': command.ON_BRIGHTNESS_LEVEL_8,
            'status': 50
        },
        'on_brightness_level_9': {
            'command': command.ON_BRIGHTNESS_LEVEL_9,
            'status': 56
        },
        'on_brightness_level_10': {
            'command': command.ON_BRIGHTNESS_LEVEL_10,
            'status': 62
        },
        'on_brightness_level_11': {
            'command': command.ON_BRIGHTNESS_LEVEL_11,
            'status': 68
        },
        'on_brightness_level_12': {
            'command': command.ON_BRIGHTNESS_LEVEL_12,
            'status': 75
        },
        'on_brightness_level_13': {
            'command': command.ON_BRIGHTNESS_LEVEL_13,
            'status': 81
        },
        'on_brightness_level_14': {
            'command': command.ON_BRIGHTNESS_LEVEL_14,
            'status': 87
        },
        'on_brightness_level_15': {
            'command': command.ON_BRIGHTNESS_LEVEL_15,
            'status': 93
        },
        'on_brightness_level_16': {
            'command': command.ON_BRIGHTNESS_LEVEL_16,
            'status': 100
        },
        'on_for_internal_time_last_brightness_level_then_off': {
            'command': command.ON_FOR_INTERNAL_TIME_LAST_BRIGHTNESS_LEVEL_THEN_OFF,
            'status': 0
        },
        'on_for_internal_time_last_brightness_level_then_previous_state': {
            'command': command.ON_FOR_INTERNAL_TIME_LAST_BRIGHTNESS_LEVEL_THEN_PREVIOUS_STATE,
            'status': None
        },
        'on_for_internal_time_then_off': {
            'command': command.ON_FOR_INTERNAL_TIME_THEN_OFF,
            'status': 0
        },
        'on_for_internal_time_then_previous_state': {
            'command': command.ON_FOR_INTERNAL_TIME_THEN_PREVIOUS_STATE,
            'status': None
        },
        'on_last_brightness_level': {
            'command': command.ON_LAST_BRIGHTNESS_LEVEL,
            'status': None
        },
        'reset': {
            'command': command.RESET,
            'status': None
        },
        'toggle': {
            'command': command.TOGGLE,
            'status': None
        },
        """
        Commands with additional byte.
        """
        'dim_brightness_level_1_in_time': {
            'command': command.DIM_BRIGHTNESS_LEVEL_1_IN_TIME,
            'status': 6
        },
        'dim_brightness_level_2_in_time': {
            'command': command.DIM_BRIGHTNESS_LEVEL_2_IN_TIME,
            'status': 12
        },
        'dim_brightness_level_3_in_time': {
            'command': command.DIM_BRIGHTNESS_LEVEL_3_IN_TIME,
            'status': 18
        },
        'dim_brightness_level_4_in_time': {
            'command': command.DIM_BRIGHTNESS_LEVEL_4_IN_TIME,
            'status': 25
        },
        'dim_brightness_level_5_in_time': {
            'command': command.DIM_BRIGHTNESS_LEVEL_5_IN_TIME,
            'status': 31
        },
        'dim_brightness_level_6_in_time': {
            'command': command.DIM_BRIGHTNESS_LEVEL_6_IN_TIME,
            'status': 37
        },
        'dim_brightness_level_7_in_time': {
            'command': command.DIM_BRIGHTNESS_LEVEL_7_IN_TIME,
            'status': 43
        },
        'dim_brightness_level_8_in_time': {
            'command': command.DIM_BRIGHTNESS_LEVEL_8_IN_TIME,
            'status': 50
        },
        'dim_brightness_level_9_in_time': {
            'command': command.DIM_BRIGHTNESS_LEVEL_9_IN_TIME,
            'status': 56
        },
        'dim_brightness_level_10_in_time': {
            'command': command.DIM_BRIGHTNESS_LEVEL_10_IN_TIME,
            'status': 62
        },
        'dim_brightness_level_11_in_time': {
            'command': command.DIM_BRIGHTNESS_LEVEL_11_IN_TIME,
            'status': 68
        },
        'dim_brightness_level_12_in_time': {
            'command': command.DIM_BRIGHTNESS_LEVEL_12_IN_TIME,
            'status': 75
        },
        'dim_brightness_level_13_in_time': {
            'command': command.DIM_BRIGHTNESS_LEVEL_13_IN_TIME,
            'status': 81
        },
        'dim_brightness_level_14_in_time': {
            'command': command.DIM_BRIGHTNESS_LEVEL_14_IN_TIME,
            'status': 87
        },
        'dim_brightness_level_15_in_time': {
            'command': command.DIM_BRIGHTNESS_LEVEL_15_IN_TIME,
            'status': 93
        },
        'dim_brightness_level_16_in_time': {
            'command': command.DIM_BRIGHTNESS_LEVEL_16_IN_TIME,
            'status': 100
        },
        'dim_down_then_off_in_time': {
            'command': command.DIM_DOWN_THEN_OFF_IN_TIME,
            'status': 0
        },
        'dim_last_brightness_level_in_time': {
            'command': command.DIM_LAST_BRIGHTNESS_LEVEL_IN_TIME,
            'status': None
        },
        'dim_last_brightness_level_then_off_in_time': {
            'command': command.DIM_LAST_BRIGHTNESS_LEVEL_THEN_OFF_IN_TIME,
            'status': 0
        },
        'dim_off_in_time': {
            'command': command.DIM_OFF_IN_TIME,
            'status': 0
        },
        'dim_then_off_in_time': {
            'command': command.DIM_THEN_OFF_IN_TIME,
            'status': 0
        },
        'dim_up_then_off_in_time': {
            'command': command.DIM_UP_THEN_OFF_IN_TIME,
            'status': 0
        },
        'off_for_time_then_last_brightness_level': {
            'command': command.OFF_FOR_TIME_THEN_LAST_BRIGHTNESS_LEVEL,
            'status': None
        },
        'on_for_time_last_brightness_level_then_off': {
            'command': command.ON_FOR_TIME_LAST_BRIGHTNESS_LEVEL_THEN_OFF,
            'status': 0
        },
        'on_for_time_last_brightness_level_then_previous_state': {
            'command': command.ON_FOR_TIME_LAST_BRIGHTNESS_LEVEL_THEN_PREVIOUS_STATE,
            'status': None
        },
        'on_for_time_then_off': {
            'command': command.ON_FOR_TIME_THEN_OFF,
            'status': 0
        },
        'on_for_time_then_previous_state': {
            'command': command.ON_FOR_TIME_THEN_PREVIOUS_STATE,
            'status': None
        },
        'set_internal_timer': {
            'command': command.SET_INTERNAL_TIMER,
            'status': None
        },
        'set_internal_timer_dim_down': {
            'command': command.SET_INTERNAL_TIMER_DIM_DOWN,
            'status': None
        },
        'set_internal_timer_dim_up': {
            'command': command.SET_INTERNAL_TIMER_DIM_UP,
            'status': None
        }
    }


class Switch(Device):
    """
    Abstraction layer for all FS20 switch devices.
    """

    callables = {
        """
        Single byte commands.
        """
        'change_internal_timer': {
            'command': command.CHANGE_INTERNAL_TIMER,
            'status': None
        },
        'educate': {
            'command': command.EDUCATE,
            'status': None
        },
        'off': {
            'command': command.OFF,
            'status': 0
        },
        'off_for_internal_time_then_last_brightness_level': {
            'command': command.OFF_FOR_INTERNAL_TIME_THEN_LAST_BRIGHTNESS_LEVEL,
            'status': None
        },
        'on': {
            'command': command.ON,
            'status': 100
        },
        'on_for_internal_time_last_brightness_level_then_off': {
            'command': command.ON_FOR_INTERNAL_TIME_LAST_BRIGHTNESS_LEVEL_THEN_OFF,
            'status': 0
        },
        'on_for_internal_time_last_brightness_level_then_previous_state': {
            'command': command.ON_FOR_INTERNAL_TIME_LAST_BRIGHTNESS_LEVEL_THEN_PREVIOUS_STATE,
            'status': None
        },
        'on_for_internal_time_then_off': {
            'command': command.ON_FOR_INTERNAL_TIME_THEN_OFF,
            'status': 0
        },
        'on_for_internal_time_then_previous_state': {
            'command': command.ON_FOR_INTERNAL_TIME_THEN_PREVIOUS_STATE,
            'status': None
        },
        'on_last_brightness_level': {
            'command': command.ON_LAST_BRIGHTNESS_LEVEL,
            'status': 100
        },
        'reset': {
            'command': command.RESET,
            'status': None
        },
        'toggle': {
            'command': command.TOGGLE,
            'status': None
        },
        """
        Commands with additional byte.
        """
        'off_for_time_then_last_brightness_level': {
            'command': command.OFF_FOR_TIME_THEN_LAST_BRIGHTNESS_LEVEL,
            'status': 100
        },
        'on_for_time_last_brightness_level_then_off': {
            'command': command.ON_FOR_TIME_LAST_BRIGHTNESS_LEVEL_THEN_OFF,
            'status': 0
        },
        'on_for_time_last_brightness_level_then_previous_state': {
            'command': command.ON_FOR_TIME_LAST_BRIGHTNESS_LEVEL_THEN_PREVIOUS_STATE,
            'status': None
        },
        'on_for_time_then_off': {
            'command': command.ON_FOR_TIME_THEN_OFF,
            'status': 0
        },
        'on_for_time_then_previous_state': {
            'command': command.ON_FOR_TIME_THEN_PREVIOUS_STATE,
            'status': None
        },
        'set_internal_timer': {
            'command': command.SET_INTERNAL_TIMER,
            'status': None
        }
    }


# Module exceptions.
class DeviceBlocked(Exception):
    pass


class UnknownCommand(Exception):
    pass