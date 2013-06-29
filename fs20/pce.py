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

from fs20 import command

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

    commands = {
        0: {
            'with_time': {
                'command': command.DIM_OFF_IN_TIME,
                'name': 'dim_off_in_time'
            },
            'without_time': {
                'command': command.OFF,
                'name': 'off'
            }
        },
        1: {
            'with_time': {
                'command': command.DIM_BRIGHTNESS_LEVEL_1_IN_TIME,
                'name': 'dim_brightness_level_1_in_time'
            },
            'without_time': {
                'command': command.ON_BRIGHTNESS_LEVEL_1,
                'name': 'on_brightness_level_1'
            }
        },
        2: {
            'with_time': {
                'command': command.DIM_BRIGHTNESS_LEVEL_2_IN_TIME,
                'name': 'dim_brightness_level_2_in_time'
            },
            'without_time': {
                'command': command.ON_BRIGHTNESS_LEVEL_2,
                'name': 'on_brightness_level_2'
            }
        },
        3: {
            'with_time': {
                'command': command.DIM_BRIGHTNESS_LEVEL_3_IN_TIME,
                'name': 'dim_brightness_level_3_in_time'
            },
            'without_time': {
                'command': command.ON_BRIGHTNESS_LEVEL_3,
                'name': 'on_brightness_level_3'
            }
        },
        4: {
            'with_time': {
                'command': command.DIM_BRIGHTNESS_LEVEL_4_IN_TIME,
                'name': 'dim_brightness_level_4_in_time'
            },
            'without_time': {
                'command': command.ON_BRIGHTNESS_LEVEL_4,
                'name': 'on_brightness_level_4'
            }
        },
        5: {
            'with_time': {
                'command': command.DIM_BRIGHTNESS_LEVEL_5_IN_TIME,
                'name': 'dim_brightness_level_5_in_time'
            },
            'without_time': {
                'command': command.ON_BRIGHTNESS_LEVEL_5,
                'name': 'on_brightness_level_5'
            }
        },
        6: {
            'with_time': {
                'command': command.DIM_BRIGHTNESS_LEVEL_6_IN_TIME,
                'name': 'dim_brightness_level_6_in_time'
            },
            'without_time': {
                'command': command.ON_BRIGHTNESS_LEVEL_6,
                'name': 'on_brightness_level_6'
            }
        },
        7: {
            'with_time': {
                'command': command.DIM_BRIGHTNESS_LEVEL_7_IN_TIME,
                'name': 'dim_brightness_level_7_in_time'
            },
            'without_time': {
                'command': command.ON_BRIGHTNESS_LEVEL_7,
                'name': 'on_brightness_level_7'
            }
        },
        8: {
            'with_time': {
                'command': command.DIM_BRIGHTNESS_LEVEL_8_IN_TIME,
                'name': 'dim_brightness_level_8_in_time'
            },
            'without_time': {
                'command': command.ON_BRIGHTNESS_LEVEL_8,
                'name': 'on_brightness_level_8'
            }
        },
        9: {
            'with_time': {
                'command': command.DIM_BRIGHTNESS_LEVEL_9_IN_TIME,
                'name': 'dim_brightness_level_9_in_time'
            },
            'without_time': {
                'command': command.ON_BRIGHTNESS_LEVEL_9,
                'name': 'on_brightness_level_9'
            }
        },
        10: {
            'with_time': {
                'command': command.DIM_BRIGHTNESS_LEVEL_10_IN_TIME,
                'name': 'dim_brightness_level_10_in_time'
            },
            'without_time': {
                'command': command.ON_BRIGHTNESS_LEVEL_10,
                'name': 'on_brightness_level_10'
            }
        },
        11: {
            'with_time': {
                'command': command.DIM_BRIGHTNESS_LEVEL_11_IN_TIME,
                'name': 'dim_brightness_level_11_in_time'
            },
            'without_time': {
                'command': command.ON_BRIGHTNESS_LEVEL_11,
                'name': 'on_brightness_level_11'
            }
        },
        12: {
            'with_time': {
                'command': command.DIM_BRIGHTNESS_LEVEL_12_IN_TIME,
                'name': 'dim_brightness_level_12_in_time'
            },
            'without_time': {
                'command': command.ON_BRIGHTNESS_LEVEL_12,
                'name': 'on_brightness_level_12'
            }
        },
        13: {
            'with_time': {
                'command': command.DIM_BRIGHTNESS_LEVEL_13_IN_TIME,
                'name': 'dim_brightness_level_13_in_time'
            },
            'without_time': {
                'command': command.ON_BRIGHTNESS_LEVEL_13,
                'name': 'on_brightness_level_13'
            }
        },
        14: {
            'with_time': {
                'command': command.DIM_BRIGHTNESS_LEVEL_14_IN_TIME,
                'name': 'dim_brightness_level_14_in_time'
            },
            'without_time': {
                'command': command.ON_BRIGHTNESS_LEVEL_14,
                'name': 'on_brightness_level_14'
            }
        },
        15: {
            'with_time': {
                'command': command.DIM_BRIGHTNESS_LEVEL_15_IN_TIME,
                'name': 'dim_brightness_level_15_in_time'
            },
            'without_time': {
                'command': command.ON_BRIGHTNESS_LEVEL_15,
                'name': 'on_brightness_level_15'
            }
        },
        16: {
            'with_time': {
                'command': command.DIM_BRIGHTNESS_LEVEL_16_IN_TIME,
                'name': 'dim_brightness_level_16_in_time'
            },
            'without_time': {
                'command': command.ON_BRIGHTNESS_LEVEL_16,
                'name': 'on_brightness_level_16'
            }
        },
        17: {
            'with_time': {
                'command': command.DIM_LAST_BRIGHTNESS_LEVEL_IN_TIME,
                'name': 'dim_last_brightness_level_in_time'
            },
            'without_time': {
                'command': command.ON_LAST_BRIGHTNESS_LEVEL,
                'name': 'on_last_brightness_level'
            }
        },
        18: {
            'with_time': {
                'command': command.DIM_LAST_BRIGHTNESS_LEVEL_THEN_OFF_IN_TIME,
                'name': 'dim_last_brightness_level_then_off_in_time'
            },
            'without_time': {
                'command': command.TOGGLE,
                'name': 'toggle'
            }
        },
        19: {
            'with_time': {
                'command': command.DIM_UP_THEN_OFF_IN_TIME,
                'name': 'dim_up_then_off_in_time'
            },
            'without_time': {
                'command': command.DIM_UP,
                'name': 'dim_up'
            }
        },
        20: {
            'with_time': {
                'command': command.DIM_DOWN_THEN_OFF_IN_TIME,
                'name': 'dim_down_then_off_in_time'
            },
            'without_time': {
                'command': command.DIM_DOWN,
                'name': 'dim_down'
            }
        },
        21: {
            'with_time': {
                'command': command.DIM_THEN_OFF_IN_TIME,
                'name': 'dim_then_off_in_time'
            },
            'without_time': {
                'command': command.DIM,
                'name': 'dim'
            }
        },
        22: {
            'with_time': {
                'command': command.SET_INTERNAL_TIMER,
                'name': 'set_internal_timer'
            },
            'without_time': {
                'command': command.CHANGE_INTERNAL_TIMER,
                'name': 'change_internal_timer'
            }
        },
        23: {
            'with_time': {
                'command': None,
                'name': None
            },
            'without_time': {
                'command': command.EDUCATE,
                'name': 'educate'
            }
        },
        24: {
            'with_time': {
                'command': command.OFF_FOR_TIME_THEN_LAST_BRIGHTNESS_LEVEL,
                'name': 'off_for_time_then_last_brightness_level'
            },
            'without_time': {
                'command': command.OFF_FOR_INTERNAL_TIME_THEN_LAST_BRIGHTNESS_LEVEL,
                'name': 'off_for_internal_time_then_last_brightness_level'
            }
        },
        25: {
            'with_time': {
                'command': command.ON_FOR_TIME_THEN_OFF,
                'name': 'on_for_time_then_off'
            },
            'without_time': {
                'command': command.ON_FOR_INTERNAL_TIME_THEN_OFF,
                'name': 'on_for_internal_time_then_off'
            }
        },
        26: {
            'with_time': {
                'command': command.ON_FOR_TIME_LAST_BRIGHTNESS_LEVEL_THEN_OFF,
                'name': 'on_for_time_last_brightness_level_then_off'
            },
            'without_time': {
                'command': command.ON_FOR_INTERNAL_TIME_LAST_BRIGHTNESS_LEVEL_THEN_OFF,
                'name': 'on_for_internal_time_last_brightness_level_then_off'
            }
        },
        27: {
            'with_time': {
                'command': None,
                'name': None
            },
            'without_time': {
                'command': command.RESET,
                'name': 'reset'
            }
        },
        28: {
            'with_time': {
                'command': command.SET_INTERNAL_TIMER_DIM_UP,
                'name': 'set_internal_timer_dim_up'
            },
            'without_time': {
                'command': None,
                'name': None
            }
        },
        29: {
            'with_time': {
                'command': command.SET_INTERNAL_TIMER_DIM_DOWN,
                'name': 'set_internal_timer_dim_down'
            },
            'without_time': {
                'command': None,
                'name': None
            }
        },
        30: {
            'with_time': {
                'command': command.ON_FOR_TIME_THEN_PREVIOUS_STATE,
                'name': 'on_for_time_then_previous_state'
            },
            'without_time': {
                'command': command.ON_FOR_INTERNAL_TIME_THEN_PREVIOUS_STATE,
                'name': 'on_for_internal_time_then_previous_state'
            }
        },
        31: {
            'with_time': {
                'command': command.ON_FOR_TIME_LAST_BRIGHTNESS_LEVEL_THEN_PREVIOUS_STATE,
                'name': 'on_for_time_last_brightness_level_then_previous_state'
            },
            'without_time': {
                'command': command.ON_FOR_INTERNAL_TIME_LAST_BRIGHTNESS_LEVEL_THEN_PREVIOUS_STATE,
                'name': 'on_for_internal_time_last_brightness_level_then_previous_state'
            }
        }
    }

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