from dropbox import client, rest, session
import json
import beanstalkc

beanstalk = beanstalkc.Connection(host='localhost')

while True:

  print "> Looking for a job"
  job = beanstalk.reserve()
  job_data = json.loads(job.body)
  job.delete()

  client = client.DropboxClient(sess)

  for search_result in client.search('', '.jpg|.png|.gif|.bmp'):
    dropbox_path = search_result['path']
    in_file = client.media(search_result['path'])['url']
    client.put_file(dropbox_path, in_file, overwrite=False)