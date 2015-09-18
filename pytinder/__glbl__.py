#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 Ritashugisha
# MIT License. <http://opensource.org/licenses/MIT>

"""
__glbl__

.. module:: __glbl__
    :platform: Linux, MacOSX, Windows
    :synopsis: Module-wide global variable storage and definition.
    :created:  2015-08-27 09:51:07
    :modified: 09-09-2015 18:14:23
.. moduleauthor:: Ritashugisha (ritashugisha@gmail.com)

"""

import os
import sys
import logging

from datetime import datetime


# Module information
MODULE_NAME = 'PyTinder'
MODULE_DOC = (
    '''{module} is a makeshift implementation of API access to Tinder through
    Facebook using Python.
For more information about {module} read the documentation.'''
).format(module=MODULE_NAME)

# Versioning information, as standardized by Semantic Versioning 2.0.0
# See <http://semver.org/> for more information
VERSIONING = (
    'devel',
    'aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo',
    'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces',
)
VERSION_DATA = {'major': 0, 'minor': 0, 'revision': '0'}
VERSION_DATA['release'] = VERSIONING[VERSION_DATA['major']]
VERSION_NUMBER = '{major}.{minor}.{revision}'.format(**VERSION_DATA)
VERSION = '{release}.{major}.{minor}r{revision}'.format(**VERSION_DATA)

# Module package information
PACKAGE = '{module}<{version}>'.format(module=MODULE_NAME, version=VERSION)

# Module author information, required some form of name and contact for backlog
AUTHOR_DATA = (
    {'name': 'Ritashugisha', 'contact': 'ritashugisha@gmail.com'},
)
AUTHOR = '\n'.join(['{name} ({contact})'.format(**_) for _ in AUTHOR_DATA])
TEAM_DATA = {
    'name': '{module} Team'.format(module=MODULE_NAME),
    'count': len(AUTHOR_DATA)
}
TEAM = '{name} ({count} members)'.format(**TEAM_DATA)

# Copyright information, MIT License <http://opensource.org/licenses/MIT>
COPYRIGHT_DATA = {'year': datetime.now().year, 'holders': TEAM}
COPYRIGHT = 'Copyright (c) {year} {holders}'.format(**COPYRIGHT_DATA)
LICENSE = '''The MIT License (MIT)

{copyright}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.'''.format(copyright=COPYRIGHT)


# Module framework variables
FROZEN = hasattr(sys, 'frozen')
DIRECTORY_PERMISSIONS = 0775

# Static module framework paths
BASE_DIR = os.path.dirname(os.path.realpath(os.path.abspath(unicode(
    (sys.executable if FROZEN else __file__), sys.getfilesystemencoding()
))))
PARENT_DIR = os.path.dirname(BASE_DIR)
STORAGE_DIR = os.path.join(
    BASE_DIR, '{}-storage'.format(MODULE_NAME.lower())
)
USER_PICKLE_DIR = os.path.join(STORAGE_DIR, 'users')

# Bootstrap variables
REQUIRED_DIRS = (STORAGE_DIR, USER_PICKLE_DIR,)
PATH_EXTENSIONS = ()
BOOTSTRAPPED = False

# Module level file paths
PATH_AUTH_STORAGE = os.path.join(STORAGE_DIR, 'auth.json')

# Module connection variables
HTTP_CONNECTION_TIMEOUT = 5

# API link variables
API_USER_AGENT = 'Tinder/3.0.4 (iPhone; iOS 7.1; Scale/2.00)'
API_USER_PLATFORM = 'ios'
API_APP_VERSION = '3'

API_BASE_URL = 'https://api.gotinder.com'
API_AUTH_URL = '{}/auth'.format(API_BASE_URL)
API_LIKE_URL = '{}/like/{{id}}'.format(API_BASE_URL)
API_DISLIKE_URL = '{}/pass/{{id}}'.format(API_BASE_URL)
API_PROFILE_URL = '{}/profile'.format(API_BASE_URL)
API_UPDATES_URL = '{}/updates'.format(API_BASE_URL)
API_USER_URL = '{}/user'.format(API_BASE_URL)

API_RECOMMENDATIONS_URL = '{}/recs'.format(API_USER_URL)
API_USER_URL = '{}/{{id}}'.format(API_USER_URL)
API_PING_URL = '{}/ping'.format(API_USER_URL)
API_MATCHES_URL = '{}/matches'.format(API_USER_URL)
API_MESSAGE_URL = API_REMOVE_URL = '{}/{{id}}'.format(API_MATCHES_URL)


FB_DEFAULT_URL = 'https://www.facebook.com/'
FB_DEVEL_CLIENT_ID = '895324067218904'
FB_PUBLIC_CLIENT_ID = '464891386855067'
FB_AUTH_URL = (
    'https://www.facebook.com/dialog/oauth?'
    'client_id={client_id}&'
    'redirect_uri=https://www.facebook.com/connect/login_success.html&'
    'scope=basic_info,email,public_profile,user_about_me,user_activities,'
    'user_birthday,user_education_history,user_friends,user_interests,'
    'user_likes,user_location,user_photos,user_relationship_details&'
    'response_type=token'
).format(client_id=FB_PUBLIC_CLIENT_ID)

# Module logging
LOGGING_LVL = logging.DEBUG
LOGGING_FMT = (
    '[%(asctime)s] [%(levelname)-8s] '
    '[%(filename)s@%(funcName)s:%(lineno)s] %(message)s'
)
logging.basicConfig(level=LOGGING_LVL, format=LOGGING_FMT)
LOG = logging.getLogger(MODULE_NAME)

# Module regex
RE_LINK = (
    r'[(http(s)?):\/\/(www\.)?a-zA-Z0-9@:%._\+~#=]{2,256}'
    r'\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)'
)
