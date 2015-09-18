#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 ritashugisha
# MIT License. <http://opensource.org/licenses/MIT>

"""
storage

.. module:: storage
    :platform: Linux, MacOSX, Windows
    :synopsis:
    :created: 09-18-2015 00:30:22
    :modified: 09-18-2015 00:30:22
.. moduleauthor:: ritashugisha (ritashugisha@gmail.com)

"""

import os
import json

import __glbl__ as glbl
import utils


class Storage(object):
    _raw = {}
    _save_to = glbl.PATH_AUTH_STORAGE

    def __init__(self):
        self._load()

    def _save(self):
        json.dump(self._raw, open(self._save_to, 'wb'))
        self._load()

    def _load(self):
        if utils.file_populated(self._save_to):
            self._raw = json.load(open(self._save_to, 'rb'))

    def store_cred(self, id, fb_user, t_token):
        glbl.LOG.debug((
            'storing credentials for user `{}` ({}) ...'
        ).format(id, fb_user))

        self._raw[id] = {'user': fb_user, 'tinder_access': t_token}
        self._save()

    def remove_cred(self, id):
        glbl.LOG.debug((
            'removing credentials for user `{}` ...'
        ).format(id, fb_user))

        del self._raw[id]
        self._save()

    def get_user(self, fb_user):
        for (k, v,) in self._raw.items():
            if 'user' in v.keys() and v['user'] == fb_user:
                return k
        return None