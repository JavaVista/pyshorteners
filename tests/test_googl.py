#!/usr/bin/env python
# encoding: utf-8
import json
import urllib

from pyshorteners.shorteners import Shortener
from pyshorteners.exceptions import (ShorteningErrorException,
                                     ExpandingErrorException)

import responses
import pytest

api_key = 'FAKE_KEY'
s = Shortener('GoogleShortener', api_key=api_key)
short_url = 'http://goo.gl/rjf0oI'
expanded = 'http://www.test.com'


@responses.activate
def test_googl_short_method():
    # mock response
    body = json.dumps(dict(id=short_url))

    url = '{}?key={}'.format(s.api_url, api_key)
    responses.add(responses.POST, url, body=body, match_querystring=True)

    shorten = s.short(expanded)
    assert shorten == short_url


@responses.activate
def test_googl_short_method_bad_response():
    # mock response
    body = dict(id=short_url)

    url = '{}?key={}'.format(s.api_url, api_key)
    responses.add(responses.POST, url, body=body, match_querystring=True)

    with pytest.raises(ShorteningErrorException):
        s.short(expanded)


@responses.activate
def test_googl_expand_method():
    # mock response
    body = json.dumps(dict(longUrl=expanded))
    param = urllib.urlencode({
        'key': api_key,
        'shortUrl': short_url,
    })
    url = '{}?{}'.format(s.api_url, param)
    responses.add(responses.GET, url, body=body, match_querystring=True)

    expanded_result = s.expand(short_url)
    assert expanded_result == expanded


@responses.activate
def test_googl_expand_method_bad_response():
    # mock response
    body = dict(longUrl=expanded)
    param = urllib.urlencode({
        'key': api_key,
        'shortUrl': short_url,
    })
    url = '{}?{}'.format(s.api_url, param)
    responses.add(responses.GET, url, body=body, match_querystring=True)

    with pytest.raises(ExpandingErrorException):
        s.expand(short_url)