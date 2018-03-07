import requests
from requests.auth import HTTPBasicAuth

import json
from agithub.GitHub import GitHub

import urllib.parse

import io
import os
import sys

# File Path
dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))

print ("running from", dirname)
print ("file is", filename)

# Encode Config
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

# agithub

# User Authentication
g = GitHub("SoapKe", "BBC19951228Soap")

# Make A Request by Github API
status, data = g.search.repositories.get(q = "language:python", sort = "stars", order = "desc", per_page = "1") 
# print(json.dumps(data, indent = 2))

# Create JSON File with a project
project_json = {}

print(json.dumps(data.get("items")[0].get("name"), indent = 2))

# Save the JSON file
# with open(os.path.join(dirname, 'python_repo_page_100_1.json'), 'w') as file:
#     file.write(json.dumps(data, indent = 2))




##### Rate Limit Testing #####

# r = requests.get('https://api.github.com/rate_limit', auth=HTTPBasicAuth('SoapKe', 'BBC19951228Soap'))
# print(r.status_code)
# print(json.loads(r.text))

# json_rate = json.loads(r.text)

# print(json.dumps(r.json(), indent = 2))