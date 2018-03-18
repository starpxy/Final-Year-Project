import requests
from requests.auth import HTTPBasicAuth

import json

import os,sys

dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))

print ("running from", dirname)
print ("file is", filename)

# Breakpoint Continuingly Test
'''
Send a http request with header which contains field 'Range'

If the server's response code is 206 (partial content) 
	-> Support 

else, the server's response code is 200, and the response header does not 
contain the field 'Content-Range' 
	-> Do not support

'''
headers = {
	'Range': 'bytes=0-4'
}

r = requests.get('https://api.github.com/repos/vinta/awesome-python/zipball', headers = headers, stream = True, auth = HTTPBasicAuth('SoapKe', 'BBC19951228Soap'))

print(type(r.status_code), r.status_code)
print(type(r.headers), r.headers)
print(type(r.cookies), r.cookies)
print(type(r.url), r.url)
print(type(r.history), r.history)

print(r.headers['content-length'])

print(r.headers['content-range'])
# with open(os.path.join(dirname, 'vinta_awesome-python.zip'), 'wb') as f:
#     f.write(r.content)