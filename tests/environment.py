# -*- coding: utf-8 -*-

import os.path
import sys

parent_dir = os.path.split(os.getcwd())[0]

if os.path.exists(os.path.join(parent_dir, 'fs20')):
    sys.path.insert(0, parent_dir)