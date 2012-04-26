#!/usr/bin/env python

from dropbox import client, session
import json
import beanstalkc
import shelve
import requests
import tempfile
import os
from face import *
from config import config

beanstalk = beanstalkc.Connection()

while True:

  print "> Looking for a job"

  job = beanstalk.reserve()
  d = shelve.open('db/tokens')
  sess = session.DropboxSession(config['APP_KEY'], config['APP_SECRET'], config['ACCESS_TYPE'])
  token = sess.obtain_access_token(d[job.body])
  c = client.DropboxClient(sess)

  for search_result in c.search('/TNW2012', '.jpg'):

    if search_result['path'].rsplit('.', 1)[1] == 'jpg':
      print('> Result:')
      print search_result

      dropbox_path = search_result['path']
      in_file = requests.get(c.media(search_result['path'])['url']).content      
      f, in_file_string = tempfile.mkstemp()

      os.write(f, in_file)
      os.close(f)

      find_faces_and_replace(in_file_string, config['replace_file'])
      
      f = open(in_file_string, 'r')
      in_file = f.read()

      f.close()      
      c.put_file(dropbox_path, in_file, overwrite=config['OVERWRITE'])

  job.delete()
