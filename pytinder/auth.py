#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 ritashugisha
# MIT License. <http://opensource.org/licenses/MIT>

"""
auth

.. module:: auth
    :platform: Linux, MacOSX, Windows
    :synopsis:
    :created: 09-17-2015 22:38:51
    :modified: 09-17-2015 22:38:51
.. moduleauthor:: ritashugisha (ritashugisha@gmail.com)

"""

import ast
import time
import json
import urlparse

import __glbl__ as glbl
import exceptions

import requests
import splinter
from bs4 import BeautifulSoup


class Tinder(object):
    _auth_url = glbl.API_AUTH_URL

    @classmethod
    def credentials(self, fb_token, fb_id):

        glbl.LOG.info((
            'retrieving `{}` Tinder credentials via `{}` ...'
        ).format(fb_id, self._auth_url))

        _t1 = time.time()
        resp = requests.post(
            self._auth_url,
            data={'facebook_token': fb_token, 'facebook_id': fb_id}
        )

        if resp.status_code == 200:
            return json.loads(resp.text)
        else:
            raise exceptions.TinderCredentialsRetrievalException((
                'failed to retrieve Tinder credentials, {}'
            ).format(resp))


class Facebook(object):
    _auth_url = glbl.FB_AUTH_URL
    _default_url = glbl.FB_DEFAULT_URL

    @classmethod
    def credentials(self, email, pass_):

        glbl.LOG.info((
            'retrieving `{}` Facebook credentials via splinter ...'
        ).format(email))

        _t1 = time.time()
        splint = splinter.Browser()

        try:
            splint.visit(self._auth_url)
            splint.fill('email', email)
            splint.fill('pass', pass_)
            splint.find_by_name('login').click()

            token = None
            for frag in urlparse.urlparse(splint.url).fragment.split('&'):
                attr = frag.split('=')
                if attr[0].lower() == 'access_token':
                    token = attr[-1]

            splint.visit(self._default_url)
            soup = BeautifulSoup(splint.html, 'lxml')
            id = str(json.loads(
                soup.find_all(
                    'a',
                    {'class': 'fbxWelcomeBoxName'}
                )[0]['data-gt']
            )['bmid'])
        except Exception as exc:
            raise exceptions.FacebookCredentialsRetrievalException((
                'failed to retrieve Facebook credentials, {}'
            ).format(exc))
        finally:
            splint.quit()

        glbl.LOG.info((
            'retrieving `{}` facebook credentials took `{} seconds` ...'
        ).format(email, time.time() - _t1))

        return {'token': token, 'id': id}
