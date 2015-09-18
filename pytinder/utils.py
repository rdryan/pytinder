#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 ritashugisha
# MIT License. <http://opensource.org/licenses/MIT>

"""
utils

.. module:: utils
    :platform: Linux, MacOSX, Windows
    :synopsis:
    :created: 09-18-2015 00:43:30
    :modified: 09-18-2015 00:43:30
.. moduleauthor:: ritashugisha (ritashugisha@gmail.com)

"""

import os


def file_exists(filepath):
    return os.path.exists(filepath) and os.path.isfile(filepath)


def file_populated(filepath):
    return file_exists(filepath) and os.stat(filepath).st_size > 0
