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
PyFS20 - Control all your FS20 devices easily with Python!

This package exports the following modules and subpackages:

    command - Holds all possible FS20 commands
    device  - Abstraction layer for FS20 devices
    pce     - Handler for device FS20 PCE (receiver)
    pcs     - Handler for device FS20 PCS (transmitter)
    util    - Utility module
"""

__all__ = ['command',
           'device',
           'pce',
           'pcs',
           'util']

import fs20.command as command
import fs20.device as device
import fs20.pce as pce
import fs20.pcs as pcs
import fs20.util as util