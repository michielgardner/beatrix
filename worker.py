#!/usr/bin/env python

from dropbox import client, rest, session
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
  job_data = json.loads(job.body)
  print job_data
  
  d = shelve.open('db/tokens.db')
  
  sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
  token = sess.obtain_access_token(d[str(job_data['oauth_token'])])
  c = client.DropboxClient(sess)

  n = 0

  for search_result in c.search('/TNW2012', '.jpg'):

    if search_result['path'].rsplit('.', 1)[1] == 'jpg':
      print('> Result:')
      print search_result

      if n % 2 == 0:
        replace_file = 'overlays/trollface1.png'
      else:
        replace_file = 'overlays/happy.png'
      
      n+=1;

      dropbox_path = search_result['path']
      in_file = requests.get(c.media(search_result['path'])['url']).content
      
      f, in_file_string = tempfile.mkstemp()
      os.write(f, in_file)
      os.close(f)

      find_faces_and_replace(in_file_string, replace_file)
      
      f = open(in_file_string, 'r')
      in_file = f.read()
      f.close()
      
      c.put_file(dropbox_path, in_file, overwrite=config['OVERWRITE'])


  job.delete()
