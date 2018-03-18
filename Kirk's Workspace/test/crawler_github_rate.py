import requests
from requests.auth import HTTPBasicAuth

import json
from agithub.GitHub import GitHub

import urllib.parse

import io
import os
import sys

##### Rate Limit Testing #####

'''
TEST RESULT
Good Internet connection 1 minute could make about 30 search requests

GITHUB RETE LIMIT
30 search requests per minute

'''

# Make A Request by Github API
for i in range(30):
	print(i)
	status, data = g.search.repositories.get(q = "language:python", sort = "stars", order = "desc", per_page = "100")
	print(status)

	r = requests.get('https://api.github.com/rate_limit', auth=HTTPBasicAuth('SoapKe', 'BBC19951228Soap'))
	print(r.status_code)
	print(json.dumps(r.headers, indent =2))
	print(json.dumps(r.json(), indent = 2))
