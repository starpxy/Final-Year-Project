import requests
from requests.auth import HTTPBasicAuth

import json

import os,sys

dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))

print ("running from", dirname)
print ("file is", filename)


r = requests.get('https://api.github.com/repos/octokit/octokit.rb/zipball', auth = HTTPBasicAuth('SoapKe', 'BBC19951228Soap'))

print(r.status_code)

# print(type(r.status_code), r.status_code)
# print(type(r.headers), r.headers)
# print(type(r.cookies), r.cookies)
# print(type(r.url), r.url)
# print(type(r.history), r.history)

with open(os.path.join(dirname, 'test.zip'), 'wb') as f:
    f.write(r.content)


# print(json.loads(r.text))

# json_rate = json.loads(r.text)

# print(json.dumps(json_rate, indent = 2))