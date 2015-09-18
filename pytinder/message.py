#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 ritashugisha
# MIT License. <http://opensource.org/licenses/MIT>

"""
message

.. module:: message
    :platform: Linux, MacOSX, Windows
    :synopsis: Define a message object.
    :created: 09-18-2015 10:42:38
    :modified: 09-18-2015 10:42:38
.. moduleauthor:: ritashugisha (ritashugisha@gmail.com)

"""

import user
import client


class Message(object):
    """ Message object definition.

    """

    _raw = None

    def __init__(self, raw):
        self._raw = raw

    def __repr__(self):
        return '<Message {self.id} ({self.src} -> {self.dst})>'.format(
            self=self
        )

    @property
    def id(self):
        return self._raw['_id']

    @property
    def match_id(self):
        return self._raw['match_id']

    @property
    def created_date(self):
        return self._raw['reated_date']

    @property
    def sent_date(self):
        return self._raw['sent_date']

    @property
    def timestamp(self):
        return self._raw['timestamp']

    @property
    def dst(self):
        return self._raw['to']

    @property
    def src(self):
        return self._raw['from']

    @property
    def message(self):
        return self._raw['message']
