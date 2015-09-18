#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 ritashugisha
# MIT License. <http://opensource.org/licenses/MIT>

"""
user

.. module:: user
    :platform: Linux, MacOSX, Windows
    :synopsis:
    :created: 09-17-2015 22:30:08
    :modified: 09-17-2015 22:30:08
.. moduleauthor:: ritashugisha (ritashugisha@gmail.com)

"""

import os
import json

try:
    import cPickle as pickle
except ImportError:
    import pickle

from bootstrap import _bootstrap
import __glbl__ as glbl
import exceptions
import storage
import utils
import auth

import requests


class Client(object):
    _raw = _id = None
    storage = None

    def __init__(self, fb_user, fb_pass=None):
        if not glbl.BOOTSTRAPPED:
            _bootstrap()

        rebuild_cred = True
        if isinstance(fb_user, basestring):
            if len(fb_user) > 0:
                self.storage = storage.Storage()
                self._id = self.storage.get_user(fb_user)

                if self.id:
                    rebuild_cred = False
                    self.deserialize()
                    if self._raw is None:
                        glbl.LOG.warning((
                            'credentials for user `{}` no longer exists, '
                            'rebuilding ...'
                        ).format(self._id))

                        self.storage.remove_cred(self._id)
                        rebuild_cred = True

                if rebuild_cred:
                    if fb_pass is not None:
                        if isinstance(fb_pass, basestring):
                            if len(fb_pass) > 0:

                                fb_cred = auth.Facebook.credentials(
                                    fb_user, fb_pass
                                )
                                self._raw = auth.Tinder.credentials(
                                    fb_cred['token'], fb_cred['id']
                                )['user']
                                self._id = self._raw['_id']

                                self.serialize()
                                self.storage.store_cred(
                                    self.id, fb_user, self.token
                                )
                            else:
                                raise exceptions.FacebookCredentialsFormatException((
                                    'missing Facebook password, '
                                    'parameter is empty'
                                ))
                        else:
                            raise exceptions.FacebookCredentialsFormatException((
                                'invalid Facebook password format, '
                                'expected password string'
                            ))
                    else:
                        raise exceptions.MissingCredentialsException((
                            'missing required Facebook password parameter'
                        ))

            else:
                raise exceptions.FacebookCredentialsFormatException((
                    'invalid passed Facebook credentials, '
                    'user empty'
                ))
        else:
            raise exceptions.FacebookCredentialsFormatException((
                'invalid passed Facebook credentials, '
                'required user string'
            ))

    def __repr__(self):
        return '<Client {self.id} ({self.full_name})>'.format(
            self=self
        )

    @property
    def id(self):
        return self._id

    @property
    def token(self):
        return self._raw['api_token']

    @property
    def name(self):
        return self._raw['name']

    @property
    def photos(self):
        return self._raw['photos']

    @property
    def full_name(self):
        return self._raw['full_name']

    @property
    def bio(self):
        return self._raw['bio']

    @property
    def gender(self):
        return self._raw['gender']

    @property
    def ping_time(self):
        return self._raw['ping_time']

    @property
    def create_date(self):
        return self._raw['create_date']

    @property
    def birth_date(self):
        return self._raw['birth_date']

    @property
    def discoverable(self):
        return self._raw['discoverable']

    @property
    def age_filter_min(self):
        return self._raw['age_filter_min']

    @property
    def age_filter_max(self):
        return self._raw['age_filter_max']

    @property
    def gender_filter(self):
        return self._raw['gender_filter']

    @property
    def distance_filter(self):
        return self._raw['distance_filter']

    @property
    def interests(self):
        return self._raw['interests']

    @property
    def _header(self):
        return {
            'X-Auth-Token': self.token,
            'user-agent': glbl.API_USER_AGENT
        }

    @property
    def _storage(self):
        return os.path.join(glbl.USER_PICKLE_DIR, '{}.pickle'.format(self.id))

    def serialize(self):
        if os.path.exists(os.path.dirname(self._storage)):
            glbl.LOG.debug((
                'serializing {} to `{}` ...'
            ).format(self, self._storage))
            pickle.dump(self, open(self._storage, 'wb'))

    def deserialize(self):
        if utils.file_exists(self._storage):
            glbl.LOG.debug((
                'deserializing user from `{}` ...'
            ).format(self._storage))
            self.__dict__.update(
                pickle.load(open(self._storage, 'rb')).__dict__
            )

    def recommendations(self):
        glbl.LOG.info((
            'retrieving recommendations for user `{}` ({}) ...'
        ).format(self.id, self.full_name))

        resp = requests.get(
            glbl.API_RECOMMENDATIONS_URL,
            headers=self._header
        )
        if resp.status_code == 200:
            return resp.json()['results']
        raise exceptions.TinderRetrievalException((
            'could not retrieve recommendations from `{}`, {}'
        ).format(glbl.API_RECOMMENDATIONS_URL, resp))

    def like(self, t_id):
        glbl.LOG.info(('liking user `{}` ...').format(t_id))

        resp = requests.get(
            glbl.API_LIKE_URL.format(id=t_id),
            header=self._header
        )
        if resp.status_code == 200:
            return resp.json()
        raise exceptions.TinderResponseException((
            'could not send like query to `{}`, {}'
        ).format(glbl.API_LIKE_URL.format(id=t_id), resp))

    def dislike(self, t_id):
        glbl.LOG.info(('disliking user `{}` ...').format(t_id))

        resp = requests.get(
            glbl.API_DISLIKE_URL.format(id=t_id),
            header=self._header
        )
        if resp.status_code == 200:
            return resp.json()
        raise exceptions.TinderResponseException((
            'could not send dislike query to `{}`, {}'
        ).format(glbl.API_LIKE_URL.format(id=t_id), resp))

    def send_message(self, t_id, message):
        glbl.LOG.info(('sending `{}` to user `{}` ...').format(message, t_id))

        resp = requests.get(
            glbl.API_MESSAGE_URL.format(id=t_id),
            headers=self._header
        )
        if resp.status_code == 200:
            return resp.json()
        raise exceptions.TinderResponseException((
            'could not send message \'{}\' query to `{}`, {}'
        ).format(message, glbl.API_LIKE_URL.format(id=t_id), resp))

    def remove(self, t_id):
        glbl.LOG.info((
            'removing user `{}` from user `{}` matches ...'
        ).format(t_id, self.id))

        resp = requests.delete(
            glbl.API_REMOVE_URL.format(id=t_id),
            headers=self._header
        )
        if resp.status_code == 200:
            return resp.json()
        raise exceptions.TinderResponseException((
            'could not remove user `{}` from user `{}` matches, {}'
        ).format(message, glbl.API_LIKE_URL.format(id=t_id), self.id, resp))

    def profile(self):
        glbl.LOG.info((
            'retrieving user `{}` (self) profile info ...'
        ).format(self.id))

        resp = requests.get(
            glbl.API_PROFILE_URL,
            headers=self._header
        )
        if resp.status_code == 200:
            return resp.json()
        raise exceptions.TinderRetrievalException((
            'could not retrieve user `{}` (self) profile info from `{}`, {}'
        ).format(self.id, glbl.API_PROFILE_URL, resp))

    def user(self, t_id):
        glbl.LOG.info((
            'retrieving user `{}` profile info ...'
        ).format(t_id))

        resp = requests.get(
            glbl.API_USER_URL.format(id=t_id),
            headers=self._header
        )
        if resp.status_code == 200:
            return resp.json()['results']
        raise exceptions.TinderRetrievalException((
            'could not retrieve user `{}` profile info from `{}`, {}'
        ).format(t_id, glbl.API_USER_URL.format(id=t_id), resp))

    def updates(self):
        glbl.LOG.info((
            'retrieving user `{}` (self) updates ...'
        ).format(self.id))

        resp = requests.post(
            glbl.API_UPDATES_URL,
            headers=self._header
        )
        if resp.status_code == 200:
            return resp.json()
        raise exceptions.TinderRetrievalException((
            'could not retrieve user `{}`(self) updates from `{}`, {}'
        ).format(self.id, glbl.API_UPDATES_URL, resp))

    def ping(self, latitude, longitude):
        if isinstance(latitude, float) and isinstance(longitude, float):
            if -90.0 < latitude < 90:
                if -180.0 < longitude < 180.0:
                    resp = requests.post(
                        glbl.API_PING_URL,
                        data={'lat': latitude, 'lon': longitude},
                        headers=self._header
                    )
                    if resp.status_code == 200:
                        return resp.json()
                    raise exceptions.TinderResponseException((
                        'could not ping location ({}, {}), {}'
                    ).format(latitude, longitude, resp))
                else:
                    raise ValueError((
                        'invalid value longitude -180 < lon < 180'
                    ))
            else:
                raise ValueError((
                    'invalid value latitude -90 < lat < 90'
                ))
        else:
            raise ValueError('invalid passed parameters, expected floats')
