#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

from usb.core import Device

import environment
from fs20.pcs import DeviceDataframeMismatch
from fs20.pcs import DeviceDataframeUnknown
from fs20.pcs import DeviceInvalidResponse
from fs20.pcs import DeviceNotFound
from fs20.pcs import InvalidInput
from fs20.pcs import PCS
from fs20.pcs import RESPONSE_OK
from fs20.pcs import RESPONSE_BUTTON_PUSH_NOT_SENT


class TestPCS(unittest.TestCase):

    def setUp(self):
        self._pcs = PCS()

    def test__get_device(self):
        self.assertTrue(isinstance(self._pcs._get_device(), Device))

    def test__get_raw_address(self):
        self.assertEqual(self._pcs._get_raw_address('\x00\x0f\xff'), '\x00\x0f\xff')
        self.assertRaises(InvalidInput, self._pcs._get_raw_address, '\x00\xff')

    def test__get_raw_command(self):
        self.assertEqual(self._pcs._get_raw_command('\x0f'), '\x0f\x00')
        self.assertEqual(self._pcs._get_raw_command('\x0f\xff'), '\x0f\xff')
        self.assertRaises(InvalidInput, self._pcs._get_raw_command, '\x00\x00\x00')

    def test__get_raw_interval(self):
        self.assertEqual(self._pcs._get_raw_interval(15), '\x0f')
        self.assertEqual(self._pcs._get_raw_interval(255), '\xff')
        self.assertRaises(InvalidInput, self._pcs._get_raw_interval, 0)
        self.assertRaises(InvalidInput, self._pcs._get_raw_interval, 256)

    def test__get_response(self):
        # Nothing sent - timeout.
        self.assertRaises(DeviceInvalidResponse, self._pcs._get_response)

    def test__write(self):
        # Indirect testing of PCS()._get_response().
        self.assertEqual(self._pcs._write('\x01\x06\xf1\x00\x00\x00\x00')[0], RESPONSE_OK)
        self.assertRaises(DeviceDataframeUnknown, self._pcs._write, '\x01\x06\xf5\x00\x00\x00\x00')
        self.assertRaises(DeviceDataframeMismatch, self._pcs._write, '\x01\x03\xf1\x00\x00\x00\x00')

    def test_get_version(self):
        self.assertEqual(self._pcs.get_version(), 'v1.1')

    def test_send_multiple(self):
        self.assertEqual(self._pcs.send_multiple('\x00\x00\x00', '\x00', 5), RESPONSE_OK)
        self.assertRaises(InvalidInput, self._pcs.send_multiple, '\x00\x00\x00', '\x00', 0)
        self.assertRaises(InvalidInput, self._pcs.send_multiple, '\x00\x00\x00', '\x00', 300)

    def test_send_once(self):
        self.assertEqual(self._pcs.send_once('\x00\x00\x00', '\x00'), RESPONSE_OK)

    def test_stop_button_push(self):
        self.assertEqual(self._pcs.stop_button_push(), RESPONSE_BUTTON_PUSH_NOT_SENT)


def get_suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestPCS)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(get_suite())