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

from fs20 import command
from fs20._device import Device


class Switch(Device):
    """
    Abstraction layer for all FS20 switch devices.
    """

    callables = {
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