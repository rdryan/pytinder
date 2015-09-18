#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 Ritashugisha
# MIT License. <http://opensource.org/licenses/MIT>

"""
__init__

.. module:: __init__
    :platform: Linux, MacOSX, Windows
    :synopsis: Module initialization header.
    :created:  2015-08-27 09:50:13
    :modified: 09-09-2015 12:18:21
.. moduleauthor:: Ritashugisha (ritashugisha@gmail.com)

"""

import __glbl__ as glbl
import exceptions
from client import Client

# Default module information
__version__ = glbl.VERSION
__copyright__ = glbl.COPYRIGHT
__license__ = glbl.LICENSE
__author__ = glbl.AUTHOR

# Overriden module information
__name__ = glbl.MODULE_NAME
__doc__ = glbl.MODULE_DOC

# Additional module information
__frozen__ = glbl.FROZEN

# Module configuration
__all__ = ('exceptions', 'client',)
