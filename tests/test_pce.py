#!/usr/bin/env python
# -*- coding: utf-8 -*-

from array import array
import unittest

from usb.core import Device

import environment
import fs20
from fs20.pce import PCE
from fs20.pce import Receiver
from fs20.pce import Response
from fs20.pcs import PCS


class TestPCE(unittest.TestCase):

    def setUp(self):
        self._pce = PCE()
        self._pcs = PCS()
        self._pce.reset()

    def test__get_device(self):
        self.assertTrue(isinstance(self._pce._get_device(), Device))

    def test_get_response(self):
        self.assertRaises(fs20.pce.DeviceInvalidResponse, self._pce.get_response)
        self.assertEqual(self._pcs.send_once('\x00\x00\x00', fs20.command.ON), fs20.pcs.RESPONSE_OK)
        self.assertEqual(self._pce.get_response().response, array('B', [17, 17, 17, 17, 17, 17, 22, 0, 0, 0, 22]))

    def test_get_version(self):
        PCE.version = None
        self.assertRaises(fs20.pce.DeviceMissingResponse, self._pce.get_version)
        self.assertEqual(self._pcs.send_once('\x00\x00\x00', fs20.command.ON), fs20.pcs.RESPONSE_OK)
        self.assertEqual(self._pce.get_response().response, array('B', [17, 17, 17, 17, 17, 17, 22, 0, 0, 0, 22]))
        self.assertEqual(self._pce.get_version(), 'v2.2')

    def test_reset(self):
        self.assertRaises(fs20.pce.DeviceInvalidResponse, self._pce.get_response)
        self.assertEqual(self._pcs.send_once('\x00\x00\x00', fs20.command.ON), fs20.pcs.RESPONSE_OK)
        self.assertEqual(self._pce.get_response().response, array('B', [17, 17, 17, 17, 17, 17, 22, 0, 0, 0, 22]))
        self.assertRaises(fs20.pce.DeviceInvalidResponse, self._pce.get_response)
        self.assertEqual(self._pcs.send_once('\x00\x00\x00', fs20.command.ON), fs20.pcs.RESPONSE_OK)
        self._pce.reset()
        self.assertRaises(fs20.pce.DeviceInvalidResponse, self._pce.get_response)


class TestReceiver(unittest.TestCase):

    def callback_address(self, response):
        raise CallbackAddress()

    def callback_address_command(self, response):
        raise CallbackAddressCommand()

    def callback_catchall(self, response):
        raise CallbackCatchall()

    def callback_command(self, response):
        raise CallbackCommand()

    def setUp(self):
        self._pce = PCE()
        self._pcs = PCS()
        self._receiver = Receiver()
        self._pce.reset()

    def test_add_callback(self):
        self.assertEqual(self._receiver.callbacks, {})
        # Callback for specific address.
        self._receiver.add_callback(self.callback_address, address='1111-1111-1111')
        self.assertEqual(self._receiver.callbacks, {'ed5ed2627e91cd1d47baead8ff7899a5': [self.callback_address]})
        # Callback for specific address and command.
        self._receiver.add_callback(self.callback_address_command, address='1111-1111-1111', command=fs20.command.ON)
        self.assertEqual(self._receiver.callbacks, { 'ed5ed2627e91cd1d47baead8ff7899a5': [self.callback_address]
                                                   , 'a08940b3a7ad5568657b5fba5db2165c': [self.callback_address_command]
                                                   })
        # Catchall callback.
        self._receiver.add_callback(self.callback_catchall)
        self.assertEqual(self._receiver.callbacks, { 'ed5ed2627e91cd1d47baead8ff7899a5': [self.callback_address]
                                                   , 'a08940b3a7ad5568657b5fba5db2165c': [self.callback_address_command]
                                                   , 'c7485dcc8d256a6f197ed7802687f252': [self.callback_catchall]
                                                   })
        # Yet another catchall callback (multiple callbacks for one request are possible and allowed).
        self._receiver.add_callback(self.callback_catchall)
        self.assertEqual(self._receiver.callbacks, { 'ed5ed2627e91cd1d47baead8ff7899a5': [self.callback_address]
                                                   , 'a08940b3a7ad5568657b5fba5db2165c': [self.callback_address_command]
                                                   , 'c7485dcc8d256a6f197ed7802687f252': [self.callback_catchall, self.callback_catchall]
                                                   })
        # Callback for specific command.
        self._receiver.add_callback(self.callback_command, command=fs20.command.ON)
        self.assertEqual(self._receiver.callbacks, { 'ed5ed2627e91cd1d47baead8ff7899a5': [self.callback_address]
                                                   , 'a08940b3a7ad5568657b5fba5db2165c': [self.callback_address_command]
                                                   , 'c7485dcc8d256a6f197ed7802687f252': [self.callback_catchall, self.callback_catchall]
                                                   , '36869acece705e939d4730507563c723': [self.callback_command]
                                                   })

    def test_run(self):
        # Callback for specific address.
        self._receiver.add_callback(self.callback_address, address='1111-1111-1111')
        self.assertEqual(self._pcs.send_once('\x00\x00\x00', fs20.command.ON), fs20.pcs.RESPONSE_OK)
        self.assertRaises(CallbackAddress, self._receiver.run)
        self._receiver.callbacks = {}
        # Callback for specific address and command.
        self._receiver.add_callback(self.callback_address_command, address='1111-1111-1111', command=fs20.command.ON)
        self.assertEqual(self._pcs.send_once('\x00\x00\x00', fs20.command.ON), fs20.pcs.RESPONSE_OK)
        self.assertRaises(CallbackAddressCommand, self._receiver.run)
        self._receiver.callbacks = {}
        # Catchall callback.
        self._receiver.add_callback(self.callback_catchall)
        self.assertEqual(self._pcs.send_once('\x00\x00\x00', fs20.command.ON), fs20.pcs.RESPONSE_OK)
        self.assertRaises(CallbackCatchall, self._receiver.run)
        self._receiver.callbacks = {}
        # Callback for specific command.
        self._receiver.add_callback(self.callback_command, command=fs20.command.ON)
        self.assertEqual(self._pcs.send_once('\x00\x00\x00', fs20.command.ON), fs20.pcs.RESPONSE_OK)
        self.assertRaises(CallbackCommand, self._receiver.run)
        self._receiver.callbacks = {}

    def test_stop(self):
        self.assertTrue(self._receiver.receiving)
        self._receiver.stop()
        self.assertFalse(self._receiver.receiving)


class TestResponse(unittest.TestCase):

    def test___init__(self):
        # Response without time value.
        response = Response(array('B', [17, 17, 17, 17, 17, 17, 22, 0, 0, 0, 22]))
        self.assertEquals(response.address, '1111-1111-1111')
        self.assertEquals(response.command, fs20.command.ON_BRIGHTNESS_LEVEL_16)
        self.assertEquals(response.name, 'ON_BRIGHTNESS_LEVEL_16')
        self.assertEquals(response.time, None)
        # Response with time value.
        response = Response(array('B', [18, 52, 18, 52, 17, 17, 4, 20, 145, 82, 22]))
        self.assertEquals(response.address, '1234-1234-1111')
        self.assertEquals(response.command, fs20.command.DIM_BRIGHTNESS_LEVEL_4_IN_TIME)
        self.assertEquals(response.name, 'DIM_BRIGHTNESS_LEVEL_4_IN_TIME')
        self.assertEquals(response.time, 12288.0)

    def test__str__(self):
        response = Response(array('B', [17, 17, 17, 17, 17, 17, 22, 0, 0, 0, 22]))
        self.assertEqual(str(response), 'Address: 1111-1111-1111, Command: ON_BRIGHTNESS_LEVEL_16, Time: None')
        response = Response(array('B', [18, 52, 18, 52, 17, 17, 4, 20, 145, 82, 22]))
        self.assertEqual(str(response), 'Address: 1234-1234-1111, Command: DIM_BRIGHTNESS_LEVEL_4_IN_TIME, Time: 12288.0')


# Test exceptions.
class CallbackAddress(Exception):
    pass


class CallbackAddressCommand(Exception):
    pass


class CallbackCatchall(Exception):
    pass


class CallbackCommand(Exception):
    pass


def get_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestPCE))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestReceiver))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestResponse))
    return suite


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(get_suite())