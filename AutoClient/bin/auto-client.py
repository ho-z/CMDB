#!/usr/bin/env python

import os
import sys

BASEDIR = sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.script import client

if __name__ == '__main__':
    client()