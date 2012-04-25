#!/usr/bin/env python

from dropbox import client, rest, session
import json
import beanstalkc
import shelve
import requests
import tempfile
import os
from face import *

APP_KEY = 'vprl6knhaaceson'
APP_SECRET = '4d0iffqqjktu1i1'
ACCESS_TYPE = 'dropbox' # ACCESS_TYPE should be 'dropbox' or 'app_folder' as configured for your app
replace_file = 'overlays/trollface1.png'

beanstalk = beanstalkc.Connection()

while True:

  print "> Looking for a job"
  job = beanstalk.reserve()
  job_data = json.loads(job.body)
  print job_data
  
  d = shelve.open('tokens')
  
  sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
  token = sess.obtain_access_token(d[str(job_data['oauth_token'])])
  c = client.DropboxClient(sess)

  for search_result in c.search('TNW2012', '.jpg'):
    print('> Result:')
    print search_result
    dropbox_path = search_result['path']
    in_file = requests.get(c.media(search_result['path'])['url']).content
    
    f, in_file_string = tempfile.mkstemp()
    os.write(f, in_file)
    os.close(f)

    find_faces_and_replace(in_file_string, replace_file)
    
    f = open(in_file_string, 'r')
    in_file = f.read()
    f.close()
    
    c.put_file(dropbox_path, in_file, overwrite=False)

  job.delete()
