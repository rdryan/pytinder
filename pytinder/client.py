#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 ritashugisha
# MIT License. <http://opensource.org/licenses/MIT>

"""
user

.. module:: user
    :platform: Linux, MacOSX, Windows
    :synopsis: Main module client.
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
import user
import match

import requests


class Client(object):
    """ Main client class for accessing personal user and Tinder functions.

    """

    _raw = _id = None
    storage = None

    def __init__(self, fb_user, fb_pass=None):
        """ Initialize client class.

        :param fb_user: Tinder user's Facebook login username
        :param fb_pass: Tinder user's Facebook login password
        :type fb_user: basestring
        :type fb_pass: basestring

        """

        if not glbl.BOOTSTRAPPED:
            _bootstrap()

        rebuild_cred = True
        if isinstance(fb_user, basestring):
            if len(fb_user) > 0:
                self.storage = storage.AuthStorage()
                self._id = self.storage.get_user(fb_user)

                # try to load user from storage (if exists)
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

                # build credentials via authentication methods
                if rebuild_cred:
                    if fb_pass is not None:
                        if isinstance(fb_pass, basestring):
                            if len(fb_pass) > 0:

                                # get facebook credentials
                                fb_cred = auth.Facebook.credentials(
                                    fb_user, fb_pass
                                )
                                # set _raw to tinder credentials
                                self._raw = auth.Tinder.credentials(
                                    fb_cred['token'], fb_cred['id']
                                )['user']
                                self._id = self._raw['_id']

                                # serialize newly build credentials
                                self.serialize()
                                self.storage.store_cred(
                                    self.id, fb_user, self.token
                                )
                            else:
                                raise exceptions.\
                                    FacebookCredentialsFormatException((
                                        'missing Facebook password, '
                                        'parameter is empty'
                                    ))
                        else:
                            raise exceptions.\
                                FacebookCredentialsFormatException((
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
        """ Custom representation of the Client.

        :rtype: string

        """

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
        """ Serialize the client object to storage.

        """

        if os.path.exists(os.path.dirname(self._storage)):
            glbl.LOG.debug((
                'serializing {} to `{}` ...'
            ).format(self, self._storage))
            pickle.dump(self, open(self._storage, 'wb'))

    def deserialize(self):
        """ Deserialize the client object from storage.

        """

        if utils.file_exists(self._storage):
            glbl.LOG.debug((
                'deserializing user from `{}` ...'
            ).format(self._storage))
            self.__dict__.update(
                pickle.load(open(self._storage, 'rb')).__dict__
            )

    def recommendations(self):
        """ Retrieve client's recommendations.

        :rtype: list of users

        """

        glbl.LOG.debug((
            'retrieving recommendations for user `{}` ({}) ...'
        ).format(self.id, self.full_name))

        resp = requests.get(
            glbl.API_RECOMMENDATIONS_URL,
            headers=self._header
        )
        if resp.status_code == 200:
            try:
                return [
                    user.User(i)
                    for i in resp.json()['results']
                    if 'tinder' not in i['user']['name'].lower()
                ]
            except KeyError:
                return []
        raise exceptions.TinderRetrievalException((
            'could not retrieve recommendations from `{}`, {}'
        ).format(glbl.API_RECOMMENDATIONS_URL, resp))

    def like(self, t_user):
        """ Like a user.

        :param t_user: Tinder user
        :type t_user: user.User
        :rtype: dict

        """

        if not isinstance(t_user, user.User) or not t_user.id:
            raise ValueError((
                'invalid user parameter, expected user.User object'
            ))
        glbl.LOG.info(('liking user `{}` ...').format(t_user))

        resp = requests.get(
            glbl.API_LIKE_URL.format(id=t_user.id),
            headers=self._header
        )
        if resp.status_code == 200:
            return resp.json()
        raise exceptions.TinderResponseException((
            'could not send like query to `{}`, {}'
        ).format(glbl.API_LIKE_URL.format(id=t_user.id), resp))

    def dislike(self, t_user):
        """ Dislike a user (pass).

        :param t_user: Tinder user
        :type t_user: user.User
        :rtype: dict

        """

        if not isinstance(t_user, user.User) or not t_user.id:
            raise ValueError((
                'invalid user parameter, expected user.User object'
            ))
        glbl.LOG.info(('disliking user `{}` ...').format(t_user))

        resp = requests.get(
            glbl.API_DISLIKE_URL.format(id=t_user.id),
            headers=self._header
        )
        if resp.status_code == 200:
            return resp.json()
        raise exceptions.TinderResponseException((
            'could not send dislike query to `{}`, {}'
        ).format(glbl.API_DISLIKE_URL.format(id=t_user.id), resp))

    def send_message(self, t_match, message):
        """ Send a message to a user match.

        :param t_match: Tinder match
        :param message: Message to be sent
        :type t_match: match.Match
        :type message: basestring
        :rtype: dict

        """

        if not isinstance(t_match, match.Match) or not t_match.id:
            raise ValueError((
                'invalid user parameter, expected match.Match object'
            ))
        if not isinstance(message, basestring) or len(message) <= 0:
            raise ValueError((
                'invalid message parameter, expected populated string'
            ))
        glbl.LOG.info((
            'sending `{}` to match `{}` ...'
        ).format(message, t_match))

        resp = requests.post(
            glbl.API_MESSAGE_URL.format(id=t_match.id),
            headers=self._header,
            data={'message': message}
        )
        if resp.status_code == 200:
            return resp.json()
        raise exceptions.TinderResponseException((
            'could not send message \'{}\' query to `{}`, {}'
        ).format(message, glbl.API_MESSAGE_URL.format(id=t_match.id), resp))

    # FIXME: Remove is possibly broken, unkown removal format
    def remove(self, t_user):
        """ Remove user match.

        :param t_user: Tinder user
        :type t_user: user.User
        :rtype: dict

        """

        if not isinstance(t_user, user.User) or not t_user.id:
            raise ValueError((
                'invalid user parameter, expected user.User object'
            ))
        glbl.LOG.info((
            'removing user `{}` from user `{}` matches ...'
        ).format(t_user, self))

        resp = requests.delete(
            glbl.API_REMOVE_URL.format(id=t_user.id),
            headers=self._header
        )
        if resp.status_code == 200:
            return resp.json()
        raise exceptions.TinderResponseException((
            'could not remove user `{}` from user `{}` matches, {}'
        ).format(t_user, self, resp))

    def profile(self):
        """ Retrieve client profile.

        :rtype: dict

        """

        glbl.LOG.debug((
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
        """ Retrieve Tinder user profile.

        :param t_id: Tinder id of the user
        :type t_id: basestring
        :rtype: dict

        """

        glbl.LOG.debug((
            'retrieving user `{}` profile info ...'
        ).format(t_id))

        resp = requests.get(
            glbl.API_USER_URL.format(id=t_id),
            headers=self._header
        )
        if resp.status_code == 200:
            return user.User(resp.json()['results'])
        raise exceptions.TinderRetrievalException((
            'could not retrieve user `{}` profile info from `{}`, {}'
        ).format(t_id, glbl.API_USER_URL.format(id=t_id), resp))

    def updates(self):
        """ Retrieve client's updates.

        ..note:: Updates also include matches and messages information.

        :rtype: dict

        """

        glbl.LOG.debug((
            'retrieving user `{}` (self) updates ...'
        ).format(self.id))

        resp = requests.post(
            glbl.API_UPDATES_URL,
            headers=self._header
        )
        if resp.status_code == 200:
            retn = resp.json()
            retn['matches'] = [match.Match(i) for i in retn['matches']]
            return retn
        raise exceptions.TinderRetrievalException((
            'could not retrieve user `{}` (self) updates from `{}`, {}'
        ).format(self.id, glbl.API_UPDATES_URL, resp))

    def ping(self, latitude, longitude):
        """ Update client location:

        :param latitude: Latitude of desired location
        :param longitude: Longitude of desired location
        :type latitude: float
        :type longitude: float
        :rtype: dict

        """

        if isinstance(latitude, float) and isinstance(longitude, float):
            if -90.0 < latitude < 90:
                if -180.0 < longitude < 180.0:
                    glbl.LOG.info((
                        'changing ping location ({}, {}) ...'
                    ).format(latitude, longitude))
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
