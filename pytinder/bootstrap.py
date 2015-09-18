#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 Ritashugisha
# MIT License. <http://opensource.org/licenses/MIT>

"""
bootstrap

.. module:: bootstrap
    :platform: Linux, MacOSX, Windows
    :synopsis: Bootstrap required resources for module.
    :created:  2015-08-27 12:12:49
    :modified: 09-10-2015 11:44:59
.. moduleauthor:: Ritashugisha (ritashugisha@gmail.com)

"""

import os
import sys
import time

import __glbl__ as glbl


def _bootstrap():
    """ Private function which sets up the module environment if required.

    """

    _t1 = time.time()
    glbl.LOG.info('bootstrapping {package} ...'.format(package=glbl.PACKAGE))

    for req in glbl.REQUIRED_DIRS:
        if not os.path.exists(req) or not os.path.isdir(req):
            glbl.LOG.debug('creating required directory `{}` ...'.format(req))
            os.makedirs(req, glbl.DIRECTORY_PERMISSIONS)

    for pth in glbl.PATH_EXTENSIONS:
        if os.path.exists(pth) and os.path.isdir(pth):
            glbl.LOG.debug('inserting additional path `{}` ...'.format(pth))
            sys.path.insert(0, pth)

    glbl.BOOTSTRAPPED = True

    glbl.LOG.debug(
        'bootstrapping {package} took `{tend}` seconds'.format(
            package=glbl.PACKAGE, tend=(time.time() - _t1)
        )
    )
