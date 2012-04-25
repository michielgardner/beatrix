#!/usr/bin/env python
from dropbox import client, rest, session
from bottle import route, run, request, template, static_file
import requests
import shelve
import json

import beanstalkc

beanstalk = beanstalkc.Connection()

APP_KEY = 'vprl6knhaaceson'
APP_SECRET = '4d0iffqqjktu1i1'
ACCESS_TYPE = 'dropbox' # ACCESS_TYPE should be 'dropbox' or 'app_folder' as configured for your app

@route('/')
def show_authorize_url():
  oauth_token = request.GET.get('oauth_token')

  sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
  d = shelve.open('tokens')

  if oauth_token is None:
    request_token = sess.obtain_request_token()
    d[request_token.key] = request_token
  else:

    bshit = {
              'oauth_token': oauth_token,
            }

    beanstalk.put(json.dumps(bshit))

  d.close()

  if oauth_token is None:
    authurl = sess.build_authorize_url(request_token, oauth_callback='http://localhost:8080/')
    return template('yeah', authurl = authurl)
  else:
    return template('done')

@route('/static/<path:path>')
def callback(path):
    return static_file(path, root='static')

run()
