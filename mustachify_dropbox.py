#!/usr/bin/env python
from dropbox import client, rest, session
from bottle import route, run, request
import requests
import shelve

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
    #sess.set_token(access_token_key, d[access_token_key])
    token = sess.obtain_access_token(d[oauth_token])
    c = client.DropboxClient(sess)

    for search_result in c.search('TNW2012', '.jpg'):
      dropbox_path = search_result['path']
      file_obj = requests.get('http://mustachify.me/?src=%s' % c.media(search_result['path'])['url']).content
      c.put_file(dropbox_path, file_obj) #, overwrite=True)

  d.close()

  if oauth_token is None:
    return '<a href="%s">Link</a>' % sess.build_authorize_url(request_token, oauth_callback='http://localhost:8080/')

run()
