# PyFS20
Control all your FS20 devices easily with Python!

### Contents
[What the...?](#what-the)  
[Currently supported devices](#currently-supported-devices)  
[Installing PyFS20](#installing-pyfs20)  
[Modules](#modules)  
....[Command](#command-view-source)  
....[Device](#device-view-source)  
....[PCE](#pce-view-source)  
....[PCS](#pcs-view-source)  
....[Util](#util-view-source)  
[Testing](#testing)

### What the...?
Are you asking yourself what the hell FS20 is? FS20 is a simple but unsecure, unidirectional radio home automation system by [ELV](http://www.elv.de/fs20-funkschaltsystem.html) and it is one of the cheapest systems to control your electrical devices (e.g. lights, shutters, ...) remotely. There are many actors and sensors available. With the USB devices [FS20 PCE](http://www.elv.de/output/controller.aspx?cid=74&detail=10&detail2=41481) (receiver) and [FS20 PCS](http://www.elv.de/output/controller.aspx?cid=74&detail=10&detail2=29530) (transmitter) it is possible to communicate to each FS20 device via your home computer. PyFS20 is a python package which allows an easy access to all this FS20 components. Build up your own programs to control your FS20 system remotely!

### Currently supported devices
Generally PyFS20 supports all devices of the FS20 system. With the modules ``fs20.pce`` and ``fs20.pcs`` you can receive or send every command which is supported by the FS20 protocol. There is also the module ``fs20.device``. This is a wrapper to have an abstract access to every FS20 switch and dimmer device. Simply use ``fs20.device.Dimmer`` to send commands to FS20 devices which controls your shutters.

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
``fs20.command`` provides all possible FS20 commands as constants. Please note that not every command is supported by a FS20 device. Have a look at the manual of your FS20 device to get a list of supported commands. This basic example prints the byte representation ``\x10`` of the command ``ON``:
``` python
import fs20

print fs20.command.ON
```

##### Device ([view source](fs20/device.py))
``fs20.device`` is an abstraction layer for FS20 devices. It allows sending commands without writing tons of code. Instantiated once, it remembers the current device status (brightness level 0-100 or ``None`` for unknown; depends from the executed command!) and allows to block the device for further commands (the instance can't execute further commands while it is blocked). Please keep in mind that this abstraction layer possibly provides more or less commands as your device actually supports. Currently there are abstraction layers for dimmer and switch devices (``fs20.device.Dimmer`` and ``fs20.device.Switch``). For shutters, simply use ``fs20.device.Dimmer`` - the commands are equal. The following example sends the command ``ON`` to the device address ``1234-1234-1111``, repeats ``DIM_DOWN`` one hundred times and dims to 100% in 4 minutes and 30 seconds:
``` python
from fs20.device import Dimmer

dimmer = Dimmer('1234-1234-1111')
dimmer.on()

dimmer.dim_down(interval=100)

dimmer.dim_brightness_level_15_in_time(time_string='00:04:30.0')
```

##### PCE ([view source](fs20/pce.py))
``fs20.pce`` is a wrapper for FS20 PCE. With ``fs20.pce.PCE`` you can receive any command which was sent to your FS20 system. The easiest way to receive commands is to use ``fs20.pce.Receiver``. This daemon thread waits for new sent commands and handles them via callbacks - each command becomes to a kind of event this way. Following exampe defines a catchall callback:
``` python
from time import sleep

import fs20
from fs20.pce import Receiver

def callback(response):
    print response

receiver = Receiver()
receiver.add_callback(callback)

receiver.start()
sleep(20)
receiver.stop()
```
The callback always has to have a ``response`` argument - ``response`` holds the response of FS20 PCE after receiving commands (have a look at ``fs20.pce.Response`` for details). After starting the receiver, the program waits 20 seconds. Within this time the function ``callback`` is triggered each time a command was received. But there are not only catchall callbacks. You also can define callbacks for a specific address, command or even both. Multiple callbacks for the same address and/or command will be called in the same order as defined.
``` python
receiver.add_callback(callback, address='1234-1234-1111')
receiver.add_callback(callback, address='1234-1234-1111', command=fs20.command.ON)
receiver.add_callback(callback, command=fs20.command.ON)
```

##### PCS ([view source](fs20/pcs.py))
``fs20.pcs`` is a wrapper for FS20 PCS. With ``fs20.pcs.PCS`` you can send any command to any device. Following example sends the command ``OFF`` to the device address ``1234-1234-1111``:
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

### Testing
To run all tests properly it is required to connect [FS20 PCS](http://www.elv.de/output/controller.aspx?cid=74&detail=10&detail2=29530) and [FS20 PCE](http://www.elv.de/output/controller.aspx?cid=74&detail=10&detail2=41481) with the machine you run the tests from. Otherwise the tests will crash. To run the tests, simply execute following commands within your shell:

``` bash
# Run all tests
cd tests && python runall.py

# Run a suite
cd tests && python test_util.py
```