#!/usr/bin/python
# -*- coding: utf-8 -*-

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


def get_suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestUtil)


if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(get_suite())