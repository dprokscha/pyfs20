#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
import unittest

import environment
from fs20 import util


class TestUtil(unittest.TestCase):

    def test_address_part_to_byte(self):
        self.assertEqual(util.address_part_to_byte(1111), '\x00')
        self.assertEqual(util.address_part_to_byte(1144), '\x0f')
        self.assertEqual(util.address_part_to_byte(4411), '\xf0')
        self.assertEqual(util.address_part_to_byte(4444), '\xff')
        self.assertEqual(util.address_part_to_byte('1111'), '\x00')
        self.assertEqual(util.address_part_to_byte('1144'), '\x0f')
        self.assertEqual(util.address_part_to_byte('4411'), '\xf0')
        self.assertEqual(util.address_part_to_byte('4444'), '\xff')

    def test_address_to_byte(self):
        self.assertEqual(util.address_to_byte('1111-1111-4444'), '\x00\x00\xff')
        self.assertEqual(util.address_to_byte('1111-1111-4411'), '\x00\x00\xf0')
        self.assertEqual(util.address_to_byte('1111-1111-1144'), '\x00\x00\x0f')
        self.assertEqual(util.address_to_byte('1111-1111-1111'), '\x00\x00\x00')
        self.assertRaises(util.InvalidInput, util.address_to_byte, '1111.1111.4444')
        self.assertRaises(util.InvalidInput, util.address_to_byte, '111.111.444')
        self.assertRaises(util.InvalidInput, util.address_to_byte, '111-111-44411')
        self.assertRaises(util.InvalidInput, util.address_to_byte, '1111-1111-4445')

    def test_byte_to_address(self):
        self.assertEqual(util.byte_to_address('\x00\x00\xff'), '1111-1111-4444')
        self.assertEqual(util.byte_to_address('\x00\x00\xf0'), '1111-1111-4411')
        self.assertEqual(util.byte_to_address('\x00\x00\x0f'), '1111-1111-1144')
        self.assertEqual(util.byte_to_address('\x00\x00\x00'), '1111-1111-1111')
        self.assertRaises(util.InvalidInput, util.byte_to_address, '\x00\x00\x00\x00')
        self.assertRaises(util.InvalidInput, util.byte_to_address, '\x00')
        self.assertRaises(util.InvalidInput, util.byte_to_address, 'foobar')
        self.assertRaises(util.InvalidInput, util.byte_to_address, 1234)

    def test_byte_to_address_part(self):
        self.assertEqual(util.byte_to_address_part('\x00'), '1111')
        self.assertEqual(util.byte_to_address_part('\x0f'), '1144')
        self.assertEqual(util.byte_to_address_part('\xf0'), '4411')
        self.assertEqual(util.byte_to_address_part('\xff'), '4444')

    def test_byte_to_time_string(self):
        self.assertEqual(util.byte_to_time_string('\x01'), '00:00:0.250')
        self.assertEqual(util.byte_to_time_string('\x0f'), '00:00:3.750')
        self.assertEqual(util.byte_to_time_string('\x1b'), '00:00:5.500')
        self.assertEqual(util.byte_to_time_string('\x2a'), '00:00:10.000')
        self.assertEqual(util.byte_to_time_string('\x5e'), '00:01:52.000')
        self.assertEqual(util.byte_to_time_string('\x99'), '00:19:12.000')
        self.assertEqual(util.byte_to_time_string('\xaa'), '00:42:40.000')
        self.assertEqual(util.byte_to_time_string('\xcf'), '04:16:0.000')

    def test_datetime_to_seconds(self):
        self.assertEqual(util.datetime_to_seconds(datetime.strptime('00:00:0.000', '%H:%M:%S.%f')), 0.0)
        self.assertEqual(util.datetime_to_seconds(datetime.strptime('00:00:0.100', '%H:%M:%S.%f')), 0.25)
        self.assertEqual(util.datetime_to_seconds(datetime.strptime('00:01:1.110', '%H:%M:%S.%f')), 61.0)
        self.assertEqual(util.datetime_to_seconds(datetime.strptime('00:01:1.130', '%H:%M:%S.%f')), 61.25)
        self.assertEqual(util.datetime_to_seconds(datetime.strptime('00:05:20.450', '%H:%M:%S.%f')), 320.5)
        self.assertEqual(util.datetime_to_seconds(datetime.strptime('01:20:12.350', '%H:%M:%S.%f')), 4812.25)

    def test_is_valid_address_part(self):
        self.assertTrue(util.is_valid_address_part('1111'))
        self.assertTrue(util.is_valid_address_part(1111))
        self.assertTrue(util.is_valid_address_part('4444'))
        self.assertTrue(util.is_valid_address_part(4444))
        self.assertFalse(util.is_valid_address_part('1181'))
        self.assertFalse(util.is_valid_address_part(1181))
        self.assertFalse(util.is_valid_address_part('1110'))
        self.assertFalse(util.is_valid_address_part(1110))
        self.assertFalse(util.is_valid_address_part('11'))
        self.assertFalse(util.is_valid_address_part(11))
        self.assertFalse(util.is_valid_address_part('11122'))
        self.assertFalse(util.is_valid_address_part(11122))

    def test_time_string_to_byte(self):
        self.assertEqual(util.time_string_to_byte('00:00:0.000'), '\x00')
        self.assertEqual(util.time_string_to_byte('00:00:0.100'), '\x01')
        self.assertEqual(util.time_string_to_byte('00:00:0.250'), '\x01')
        self.assertEqual(util.time_string_to_byte('00:00:3.750'), '\x0f')
        self.assertEqual(util.time_string_to_byte('00:00:5.500'), '\x1b')
        self.assertEqual(util.time_string_to_byte('00:00:10.000'), '\x2a')
        self.assertEqual(util.time_string_to_byte('00:01:52.000'), '\x5e')
        self.assertEqual(util.time_string_to_byte('00:19:12.000'), '\x99')
        self.assertEqual(util.time_string_to_byte('00:42:40.000'), '\xaa')
        self.assertEqual(util.time_string_to_byte('04:16:0.000'), '\xcf')
        self.assertRaises(util.InvalidInput, util.time_string_to_byte, '04:16:5.000')


def get_suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestUtil)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(get_suite())