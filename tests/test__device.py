#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

import environment
import fs20
from fs20.pcs import PCS
from fs20.switch import Switch


class TestDevice(unittest.TestCase):

    def setUp(self):
        self._pcs = PCS()
        self._switch = Switch('1111-1111-1111')

    def test_callable(self):
        self.assertEqual(self._switch.on(), 100)
        self.assertEqual(self._switch.off(), 0)
        self.assertEqual(self._switch.reset(), None)
        self.assertEqual(self._pcs.stop_multiple_sending(), fs20.pcs.RESPONSE_STOP_MULTIPLE_SENDING_NOT_SENT)
        self.assertEqual(self._switch.on(interval=100), 100)
        self.assertEqual(self._pcs.stop_multiple_sending(), fs20.pcs.RESPONSE_STOP_MULTIPLE_SENDING_OK)

    def test_callable_blocked(self):
        self.assertEqual(self._switch.on(), 100)
        self._switch.blocked = True
        self.assertRaises(fs20._device.DeviceBlocked, self._switch.on)

    def test_callable_unknown(self):
        def unknown_command():
            self._switch.foobar()
        self.assertRaises(fs20._device.UnknownCommand, unknown_command)


def get_suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestDevice)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(get_suite())