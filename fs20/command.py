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

"""
Single byte commands.
"""
# Must be send before and after SET_INTERNAL_TIMER.
CHANGE_INTERNAL_TIMER = '\x16'
# Dim one level down.
DIM_DOWN = '\x14'
# Dim one level up.
DIM_UP = '\x13'
# Dim stepwise up (to maximum) or down (to minimum).
DIM = '\x15'
# Can be used to educate an address (does not work for all FS20 devices).
EDUCATE = '\x17'
# Turn off.
OFF = '\x00'
# Turn off for internal time, then turn on to last brightness level.
OFF_FOR_INTERNAL_TIME_THEN_LAST_BRIGHTNESS_LEVEL = '\x18'
# Turn on (similar to ON_BRIGHTNESS_LEVEL_16).
ON = '\x10'
# Turn on, set brightness level to 1 (6,25% minimum).
ON_BRIGHTNESS_LEVEL_1 = '\x01'
# Turn on, set brightness level to 2 (12,5%).
ON_BRIGHTNESS_LEVEL_2 = '\x02'
# Turn on, set brightness level to 3 (18,75%).
ON_BRIGHTNESS_LEVEL_3 = '\x03'
# Turn on, set brightness level to 4 (25%).
ON_BRIGHTNESS_LEVEL_4 = '\x04'
# Turn on, set brightness level to 5 (31,25%).
ON_BRIGHTNESS_LEVEL_5 = '\x05'
# Turn on, set brightness level to 6 (37,5%).
ON_BRIGHTNESS_LEVEL_6 = '\x06'
# Turn on, set brightness level to 7 (43,75%).
ON_BRIGHTNESS_LEVEL_7 = '\x07'
# Turn on, set brightness level to 8 (50%).
ON_BRIGHTNESS_LEVEL_8 = '\x08'
# Turn on, set brightness level to 9 (56,25%).
ON_BRIGHTNESS_LEVEL_9 = '\x09'
# Turn on, set brightness level to 10 (62,5%).
ON_BRIGHTNESS_LEVEL_10 = '\x0a'
# Turn on, set brightness level to 11 (68,75%).
ON_BRIGHTNESS_LEVEL_11 = '\x0b'
# Turn on, set brightness level to 12 (75%).
ON_BRIGHTNESS_LEVEL_12 = '\x0c'
# Turn on, set brightness level to 13 (81,25%).
ON_BRIGHTNESS_LEVEL_13 = '\x0d'
# Turn on, set brightness level to 14 (87,5%).
ON_BRIGHTNESS_LEVEL_14 = '\x0e'
# Turn on, set brightness level to 15 (93,75%).
ON_BRIGHTNESS_LEVEL_15 = '\x0f'
# Turn on, set brightness level to 16 (100% maximum).
ON_BRIGHTNESS_LEVEL_16 = '\x10'
# Turn on for internal time to last brightness level, then turn off.
ON_FOR_INTERNAL_TIME_LAST_BRIGHTNESS_LEVEL_THEN_OFF = '\x1a'
# Turn on (100%) for internal time to last brightness level, then previous state.
ON_FOR_INTERNAL_TIME_LAST_BRIGHTNESS_LEVEL_THEN_PREVIOUS_STATE = '\x1f'
# Turn on for internal time, then turn off.
ON_FOR_INTERNAL_TIME_THEN_OFF = '\x19'
# Turn on for internal time, then previous state.
ON_FOR_INTERNAL_TIME_THEN_PREVIOUS_STATE = '\x1e'
# Turn on to last brightness level.
ON_LAST_BRIGHTNESS_LEVEL = '\x11'
# Reset to factory settings (does not work for all FS20 devices).
RESET = '\x1b'
# Toggle between off and on (previous state).
TOGGLE = '\x12'

"""
Commands with additional byte. The additional byte is always a time value. Time
values between 250 milliseconds and 4 hours, 16 minutes are possible. "fs20.util"
provides methods to convert time values to their byte representation.
"""
# Dim to brightness level 1 (6,25%) in the given time.
DIM_BRIGHTNESS_LEVEL_1_IN_TIME = '\x21'
# Dim to brightness level 2 (12,5%) in the given time.
DIM_BRIGHTNESS_LEVEL_2_IN_TIME = '\x22'
# Dim to brightness level 3 (18,75%) in the given time.
DIM_BRIGHTNESS_LEVEL_3_IN_TIME = '\x23'
# Dim to brightness level 4 (25%) in the given time.
DIM_BRIGHTNESS_LEVEL_4_IN_TIME = '\x24'
# Dim to brightness level 5 (31,25%) in the given time.
DIM_BRIGHTNESS_LEVEL_5_IN_TIME = '\x25'
# Dim to brightness level 6 (37,5%) in the given time.
DIM_BRIGHTNESS_LEVEL_6_IN_TIME = '\x26'
# Dim to brightness level 7 (43,75%) in the given time.
DIM_BRIGHTNESS_LEVEL_7_IN_TIME = '\x27'
# Dim to brightness level 8 (50%) in the given time.
DIM_BRIGHTNESS_LEVEL_8_IN_TIME = '\x28'
# Dim to brightness level 9 (56,25%) in the given time.
DIM_BRIGHTNESS_LEVEL_9_IN_TIME = '\x29'
# Dim to brightness level 10 (62,5%) in the given time.
DIM_BRIGHTNESS_LEVEL_10_IN_TIME = '\x2a'
# Dim to brightness level 11 (68,75%) in the given time.
DIM_BRIGHTNESS_LEVEL_11_IN_TIME = '\x2b'
# Dim to brightness level 12 (75%) in the given time.
DIM_BRIGHTNESS_LEVEL_12_IN_TIME = '\x2c'
# Dim to brightness level 13 (81,25%) in the given time.
DIM_BRIGHTNESS_LEVEL_13_IN_TIME = '\x2d'
# Dim to brightness level 14 (87,5%) in the given time.
DIM_BRIGHTNESS_LEVEL_14_IN_TIME = '\x2e'
# Dim to brightness level 15 (93,75%) in the given time.
DIM_BRIGHTNESS_LEVEL_15_IN_TIME = '\x2f'
# Dim to brightness level 16 (100%) in the given time.
DIM_BRIGHTNESS_LEVEL_16_IN_TIME = '\x30'
# Dim one level down, then turn off after the given time.
DIM_DOWN_THEN_OFF_IN_TIME = '\x34'
# Dim up or down to last brightness level in the given time.
DIM_LAST_BRIGHTNESS_LEVEL_IN_TIME = '\x31'
# Dim to last brightness leven, then turn off after the given time.
DIM_LAST_BRIGHTNESS_LEVEL_THEN_OFF_IN_TIME = '\x32'
# Dim to 0% in the given time.
DIM_OFF_IN_TIME = '\x20'
# Dim one level up (to maximum) or down (to minimum) in change, then turn off after the given time.
DIM_THEN_OFF_IN_TIME = '\x35'
# Dim one level up, then turn off after the given time.
DIM_UP_THEN_OFF_IN_TIME = '\x33'
# Turn off for given time, then turn on to last brightness level.
OFF_FOR_TIME_THEN_LAST_BRIGHTNESS_LEVEL = '\x38'
# Turn on (last brightness level) for given time, then turn off.
ON_FOR_TIME_LAST_BRIGHTNESS_LEVEL_THEN_OFF = '\x3a'
# Turn on (last brightness level) for given time, then previous state.
ON_FOR_TIME_LAST_BRIGHTNESS_LEVEL_THEN_PREVIOUS_STATE = '\x3f'
# Turn on (100%) for given time, then turn off.
ON_FOR_TIME_THEN_OFF = '\x39'
# Turn on (100%) for given time, then previous state.
ON_FOR_TIME_THEN_PREVIOUS_STATE = '\x3e'
# Set internal timer (used for single byte commands depends on internal timer).
SET_INTERNAL_TIMER = '\x36'
# Set internal timer to dim down.
SET_INTERNAL_TIMER_DIM_DOWN = '\x3d'
# Set internal timer to dim up.
SET_INTERNAL_TIMER_DIM_UP = '\x3c'