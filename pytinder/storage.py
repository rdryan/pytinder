#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 ritashugisha
# MIT License. <http://opensource.org/licenses/MIT>

"""
storage

.. module:: storage
    :platform: Linux, MacOSX, Windows
    :synopsis: Provide authentication storage objects.
    :created: 09-18-2015 00:30:22
    :modified: 09-18-2015 00:30:22
.. moduleauthor:: ritashugisha (ritashugisha@gmail.com)

"""

import os
import json

import __glbl__ as glbl
import utils


class AuthStorage(object):
    """ Authorization storage for client Facebook and Tinder access.

    """

    _raw = {}
    _save_to = glbl.PATH_AUTH_STORAGE

    def __init__(self):
        self._load()

    @property
    def raw(self):
        return self._raw

    def _save(self):
        """ Save the raw dict to storage.

        """

        json.dump(self._raw, open(self._save_to, 'wb'))
        self._load()

    def _load(self):
        """ Load the raw dict from storage.

        """

        if utils.file_populated(self._save_to):
            self._raw = json.load(open(self._save_to, 'rb'))

    def store_cred(self, fb_user, fb_token, fb_id, t_token, t_id):
        """ Build credential storage for access tokens.

        :param fb_user: Client Facebook login username
        :param fb_token: Client Facebook access token
        :param fb_id: Client Facebook id
        :param t_token: Client Tinder access token
        :param t_id: Client Tinder id

        """

        glbl.LOG.debug((
            'storing credentials for user `{}` ({}) ...'
        ).format(t_id, fb_user))

        self._raw[t_id] = {
            'user': fb_user,
            'tinder_access': t_token,
            'facebook_access': fb_token,
            'facebook_id': fb_id
        }
        self._save()

    def remove_cred(self, id):
        """ Remove credential from storage.

        :param id: Client Tinder id
        :type id: basestring

        """

        glbl.LOG.debug((
            'removing credentials for user `{}` ...'
        ).format(id, fb_user))

        del self._raw[id]
        self._save()

    def get_user(self, fb_user):
        """ Retrieve a user's Tinder id via Facebook username.

        :param fb_user: Client Facebook login username
        :type fb_user: basestring
        :rtype: basestring

        """

        for (k, v,) in self._raw.items():
            if 'user' in v.keys() and v['user'] == fb_user:
                return k
        return None
