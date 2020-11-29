#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

from core.src import run


if __name__ == "__main__":

    run()
