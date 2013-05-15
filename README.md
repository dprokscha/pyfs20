# PyFS20
Easy access to all your FS20 devices.

###What the...?
Are you asking yourself what the hell FS20 is? Well, here is the answer: FS20 is a simple but unsecure, unidirectional radio home automation system by [eQ-3](http://www.eQ-3.de). It is sold by online shops like [ELV](http://www.elv.de/fs20-funkschaltsystem.html) and it is one of the cheapest systems to control your electrical devices (e.g. lights, shutters, ...) remotly. There are many actors and sensors available. With the USB devices [FS20 PCE](http://www.elv.de/output/controller.aspx?cid=74&detail=10&detail2=41481) (receiver) and [FS20 PCS](http://www.elv.de/output/controller.aspx?cid=74&detail=10&detail2=29530) (transmitter) it is possible to communicate to each FS20 device via computer. PyFS20 is a python package which allows an easy access to all this FS20 components. Build up your own programs to control your FS20 system remotely!

###Currently supported devices
Generally PyFS20 supports all devices of FS20 system. With the sub-packages ``PCE`` and ``PCS`` you can receive or send every command which is supported by the FS20 protocol. There are also the sub-packages ``Switch`` and ``Dimmer``. These are wrappers to have an abstract access to every FS20 switch and dimmer device. Simply use ``Dimmer`` to send commands to FS20 devices which controls your shutters.

#####FS20 PCS
This sends the command ``OFF`` to the device address ``1234-1234-1111``:
``` python
import fs20
from fs20.pcs import PCS

address = fs20.util.address_part_to_byte('1234') + \
          fs20.util.address_part_to_byte('1234') + \
          fs20.util.address_part_to_byte('1111')

pcs = PCS()
pcs.send_once(address, fs20.command.ON)
```