#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2014 ritashugisha
# MIT License. <http://opensource.org/licenses/MIT>

"""
exceptions

.. module:: exceptions
    :platform: Linux, MacOSX, Windows
    :synopsis: Define custom module level exceptions.
    :created: 09-17-2015 22:33:12
    :modified: 09-17-2015 22:33:12
.. moduleauthor:: ritashugisha (ritashugisha@gmail.com)

"""


class TinderBotException(Exception):
    _code = 9100

    def __init__(self, message, code=None):
        super(TinderBotException, self).__init__(message)
        self.code = (code if code else self._code)


class CredentialsException(TinderBotException):
    _code = 9300


class CredentialsFormatException(CredentialsException):
    _code = 9310


class TinderCredentialsFormatException(CredentialsFormatException):
    _code = 9311


class FacebookCredentialsFormatException(CredentialsFormatException):
    _code = 9312


class MissingCredentialsException(CredentialsException):
    _code = 9320


class CredentialsRetrievalException(CredentialsException):
    _code = 9330


class TinderCredentialsRetrievalException(CredentialsRetrievalException):
    _code = 9331


class FacebookCredentialsRetrievalException(CredentialsRetrievalException):
    _code = 9332


class RetrievalException(TinderBotException):
    _code = 9200


class TinderRetrievalException(RetrievalException):
    _code = 9201


class ResponseException(TinderBotException):
    _code = 9210


class TinderResponseException(ResponseException):
    _code = 9211
