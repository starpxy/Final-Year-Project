import requests
from requests.auth import HTTPBasicAuth

import json

##### Rate Limit Testing #####

'''
TEST RESULT
Good Internet connection 1 minute could make about 30 search requests

GITHUB RETE LIMIT
30 search requests per minute

'''

# Make A Request by Github API
# https://api.github.com/search/repositories?q=language%3Apython&sort=stars&order=desc&page=2
# https://api.github.com/search/repositories?q=language:python&sort=stars&order=desc

r = requests.get('https://api.github.com/search/repositories?q=language:python&sort=stars&order=desc&per_page=100&page=10', auth=HTTPBasicAuth('SoapKe', 'BBC19951228Soap'))
print(r.status_code)
print(r.headers)
print(json.dumps(r.json(), indent = 2))
