#!/usr/bin/env python
from dropbox import client, rest, session
from bottle import route, run, request
import requests

APP_KEY = 'vprl6knhaaceson'
APP_SECRET = '4d0iffqqjktu1i1'
ACCESS_TYPE = 'dropbox' # ACCESS_TYPE should be 'dropbox' or 'app_folder' as configured for your app

@route('/')
def show_authorize_url():
  sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
  request_token = sess.obtain_request_token()

  return sess.build_authorize_url(request_token, oauth_callback='http://localhost:8080/mustachify/')

@route('/mustachify/')
def mustachify():
  uid = request.GET.get('uid')
  oauth_token = request.GET.get('oauth_token')
  
  access_token = sess.obtain_access_token(request_token)
  #client = client.DropboxClient(sess)

  #for search_result in client.search('TNW2012', '.jpg'):
  #  dropbox_path = search_result['path']
  #  file_obj = requests.get('http://mustachify.me/?src=%s' % client.media(search_result['path'])['url']).content

  #  client.put_file(dropbox_path, file_obj, overwrite=True)

run()
