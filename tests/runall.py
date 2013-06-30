#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import glob
import os.path

if __name__ == '__main__':
    suite = unittest.TestSuite()
    for i in glob.glob('test_*.py'):
        module = __import__(os.path.splitext(i)[0])
        if hasattr(module, 'get_suite'):
            suite.addTest(module.get_suite())
    unittest.TextTestRunner(verbosity=2).run(suite)