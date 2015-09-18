#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 ritashugisha
# MIT License. <http://opensource.org/licenses/MIT>

"""
match

.. module:: match
    :platform: Linux, MacOSX, Windows
    :synopsis: Define a match object.
    :created: 09-18-2015 10:30:32
    :modified: 09-18-2015 10:30:32
.. moduleauthor:: ritashugisha (ritashugisha@gmail.com)

"""

import user
import message


class Match(object):
    """ Match object definition.

    """

    _raw = None

    def __init__(self, raw):
        self._raw = raw

    def __repr__(self):
        return '<Match {self.id} ({self.person})>'.format(self=self)

    @property
    def id(self):
        return self._raw['_id']

    @property
    def match_id(self):
        return self._raw['id']

    @property
    def dead(self):
        return self._raw['dead']

    @property
    def closed(self):
        return self._raw['closed']

    @property
    def pending(self):
        return self._raw['pending']

    @property
    def super_like(self):
        return self._raw['is_super_like']

    @property
    def following(self):
        return self._raw['following']

    @property
    def following_moments(self):
        return self._raw['following_moments']

    @property
    def created_date(self):
        return self._raw['created_date']

    @property
    def participants(self):
        return self._raw['participants']

    @property
    def person(self):
        return user.User(self._raw['person'])

    @property
    def common_friend_count(self):
        return self._raw['common_friend_count']

    @property
    def common_like_count(self):
        return self._raw['common_like_count']

    @property
    def messages(self):
        return [message.Message(i) for i in self._raw['messages']]
