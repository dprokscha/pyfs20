#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

from usb.core import Device

import environment
import fs20
from fs20.pcs import PCS


class TestPCS(unittest.TestCase):

    def setUp(self):
        self.__pcs = PCS()

    def test___get_device(self):
        self.assertTrue(isinstance(self.__pcs._PCS__get_device(), Device))

    def test___get_raw_address(self):
        self.assertEqual(self.__pcs._PCS__get_raw_address('\x00\x0f\xff'), '\x00\x0f\xff')
        self.assertRaises(fs20.pcs.InvalidInput, self.__pcs._PCS__get_raw_address, '\x00\xff')

    def test___get_raw_command(self):
        self.assertEqual(self.__pcs._PCS__get_raw_command('\x0f'), '\x0f\x00')
        self.assertEqual(self.__pcs._PCS__get_raw_command('\x0f\xff'), '\x0f\xff')
        self.assertRaises(fs20.pcs.InvalidInput, self.__pcs._PCS__get_raw_command, '\x00\x00\x00')

    def test___get_raw_interval(self):
        self.assertEqual(self.__pcs._PCS__get_raw_interval(15), '\x0f')
        self.assertEqual(self.__pcs._PCS__get_raw_interval(255), '\xff')
        self.assertRaises(fs20.pcs.InvalidInput, self.__pcs._PCS__get_raw_interval, 0)
        self.assertRaises(fs20.pcs.InvalidInput, self.__pcs._PCS__get_raw_interval, 256)

    def test___get_response(self):
        # Nothing sent - timeout.
        self.assertRaises(fs20.pcs.DeviceInvalidResponse, self.__pcs._PCS__get_response)

    def test___write(self):
        # Indirect testing of PCS()._get_response().
        self.assertEqual(self.__pcs._PCS__write('\x01\x06\xf1\x00\x00\x00\x00')[0], fs20.pcs.RESPONSE_OK)
        self.assertRaises(fs20.pcs.DeviceDataframeUnknown, self.__pcs._PCS__write, '\x01\x06\xf5\x00\x00\x00\x00')
        self.assertRaises(fs20.pcs.DeviceDataframeMismatch, self.__pcs._PCS__write, '\x01\x03\xf1\x00\x00\x00\x00')
        self.assertEqual(self.__pcs._PCS__write('\xff\x00', False)[0], fs20.pcs.RESPONSE_OK)

    def test_get_version(self):
        self.assertEqual(self.__pcs.get_version(), 'v1.7')

    def test_send_multiple(self):
        self.assertEqual(self.__pcs.send_multiple('\x00\x00\x00', fs20.command.DIM_DOWN, interval=5), fs20.pcs.RESPONSE_OK)
        self.assertRaises(fs20.pcs.InvalidInput, self.__pcs.send_multiple, '\x00\x00\x00', fs20.command.ON, interval=0)
        self.assertRaises(fs20.pcs.InvalidInput, self.__pcs.send_multiple, '\x00\x00\x00', fs20.command.ON, interval=300)

    def test_send_once(self):
        self.assertEqual(self.__pcs.send_once('\x00\x00\x00', fs20.command.ON), fs20.pcs.RESPONSE_OK)

    def test_stop_multiple_sending(self):
        self.assertEqual(self.__pcs.stop_multiple_sending(), fs20.pcs.RESPONSE_STOP_MULTIPLE_SENDING_NOT_SENT)
        self.assertEqual(self.__pcs.send_multiple('\x00\x00\x00', fs20.command.DIM_DOWN, interval=100), fs20.pcs.RESPONSE_OK)
        self.assertEqual(self.__pcs.stop_multiple_sending(), fs20.pcs.RESPONSE_STOP_MULTIPLE_SENDING_OK)


def get_suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestPCS)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(get_suite())