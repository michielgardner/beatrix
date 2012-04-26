#!/usr/bin/env python
from dropbox import session
from bottle import route, run, request, template, static_file
import requests
import shelve
from config import config
import beanstalkc

beanstalk = beanstalkc.Connection()

@route('/')
def show_authorize_url():
  oauth_token = request.GET.get('oauth_token')
  sess = session.DropboxSession(config['APP_KEY'], config['APP_SECRET'], config['ACCESS_TYPE'])
  d = shelve.open('db/tokens')

  if oauth_token is None:
    request_token = sess.obtain_request_token()
    d[request_token.key] = request_token
  else:
    beanstalk.put(oauth_token)

  d.close()

  if oauth_token is None:
    return template('yeah', authorize_url = sess.build_authorize_url(request_token, oauth_callback='http://localhost:8080/'))
  else:
    return template('done')

@route('/static/<path:path>')
def callback(path):
    return static_file(path, root='static')

run()
