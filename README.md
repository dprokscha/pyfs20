# PyFS20
Easy access to all your FS20 devices.

### Contents
[What the...?](#what-the)  
[Currently supported devices](#currently-supported-devices)  
[Installing PyFS20](#installing-pyfs20)  
[Modules](#modules)  
....[Command](#command-view-source)  
....[PCS](#pcs-view-source)  
....[Util](#util-view-source)

### What the...?
Are you asking yourself what the hell FS20 is? FS20 is a simple but unsecure, unidirectional radio home automation system by [eQ-3](http://www.eQ-3.de). It is sold by online shops like [ELV](http://www.elv.de/fs20-funkschaltsystem.html) and it is one of the cheapest systems to control your electrical devices (e.g. lights, shutters, ...) remotly. There are many actors and sensors available. With the USB devices [FS20 PCE](http://www.elv.de/output/controller.aspx?cid=74&detail=10&detail2=41481) (receiver) and [FS20 PCS](http://www.elv.de/output/controller.aspx?cid=74&detail=10&detail2=29530) (transmitter) it is possible to communicate to each FS20 device via your home computer. PyFS20 is a python package which allows an easy access to all this FS20 components. Build up your own programs to control your FS20 system remotely!

### Currently supported devices
Generally PyFS20 supports all devices of FS20 system. With the modules ``PCE`` and ``PCS`` you can receive or send every command which is supported by the FS20 protocol. There are also the modules ``Switch`` and ``Dimmer``. These are wrappers to have an abstract access to every FS20 switch and dimmer device. Simply use ``Dimmer`` to send commands to FS20 devices which controls your shutters.

### Installing PyFS20
PyFS20 requires Python 2.6 (or higher) and PyUSB to run properly.

Simply do the following:
* [Install Python 2.6 (or higher)](http://www.python.org/getit/)
* [Install PyUSB](https://github.com/walac/pyusb)
* [Download PyFS20](https://github.com/dprokscha/pyfs20/archive/master.zip)
* Follow the code examples in this README

Please note: I didn't tested this package with Python 3.0 (or higher).

### Modules
Please have a look inside the code of the modules to get an overview about available methods and what they do. The code is documented pretty well. In this README you only get some basic examples how to use the modules.

##### Command ([view source](fs20/command.py))
Provides all possible FS20 commands as constants. Please note that not every command is supported by a FS20 device. Have a look at the manual of your FS20 device to get a list of supported commands. This basic example prints the byte representation ``\x10`` of the command ``ON``:
``` python
import fs20

print fs20.command.ON
```

##### PCS ([view source](fs20/pcs.py))
This module is a wrapper for FS20 PCS. With ``PCS`` you can send any command to any device. Following example sends the command ``OFF`` to the device address ``1234-1234-1111``:
``` python
import fs20
from fs20.pcs import PCS

address = fs20.util.address_to_byte('1234-1234-1111')
time = fs20.util.time_string_to_byte('00:00:2.0')

pcs = PCS()
pcs.send_once(address, fs20.command.OFF)

pcs.send_once(address, fs20.command.DIM_BRIGHTNESS_LEVEL_16_IN_TIME, time)
```

##### Util ([view source](fs20/util.py))
Holds some generic methods. Most of them handles conversion of FS20 addresses and times. The following example converts the address part ``4444`` to its byte representation ``\xff``:
``` python
import fs20

print fs20.util.address_part_to_byte('4444')
```
