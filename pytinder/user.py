#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 ritashugisha
# MIT License. <http://opensource.org/licenses/MIT>

"""
user

.. module:: user
    :platform: Linux, MacOSX, Windows
    :synopsis: Define a user object.
    :created: 09-18-2015 10:00:50
    :modified: 09-18-2015 10:00:50
.. moduleauthor:: ritashugisha (ritashugisha@gmail.com)

"""


class User(object):
    """ User object definition.

    """

    _raw = None

    def __init__(self, raw):
        self._raw = raw

    def __repr__(self):
        return '<User {self.id} ({self.name})>'.format(self=self)

    @property
    def id(self):
        return self._raw['_id']

    @property
    def name(self):
        return self._raw['name']

    @property
    def bio(self):
        return self._raw['bio']

    @property
    def gender(self):
        return self._raw['gender']

    @property
    def badges(self):
        if 'badges' in self._raw.keys():
            return self._raw['badges']
        return None

    @property
    def distance_mi(self):
        return self._raw['distance_mi']

    @property
    def birth_date(self):
        return self._raw['birth_date']

    @property
    def birth_date_info(self):
        return self._raw['birth_date_info']

    @property
    def instagram(self):
        if 'instagram' in self._raw.keys():
            return self._raw['instagram']
        return None

    @property
    def photos(self):
        return self._raw['photos']

    @property
    def connection_count(self):
        return self._raw['connection_count']

    @property
    def common_like_count(self):
        return self._raw['common_like_count']

    @property
    def common_likes(self):
        return self._raw['common_likes']

    @property
    def common_friend_count(self):
        return self._raw['common_friend_count']

    @property
    def common_friends(self):
        return self._raw['common_friends']

    @property
    def ping_time(self):
        return self._raw['ping_time']
