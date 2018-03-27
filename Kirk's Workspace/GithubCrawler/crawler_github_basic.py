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

output_dirname = dirname + "\\python"

# Encode Config
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

# agithub

# User Authentication
g = GitHub("SoapKe", "BBC19951228Soap")

# Make A Request by Github API
for i in range(30):
	print(i)
	status, data = g.search.repositories.get(q = "language:python", sort = "stars", order = "desc", per_page = "1")
	print(status)

	r = requests.get('https://api.github.com/rate_limit', auth=HTTPBasicAuth('SoapKe', 'BBC19951228Soap'))
	print(r.status_code)
	print(json.dumps(r.json(), indent = 2))

# print(json.dumps(data, indent = 2))

# for i in range(100):
# 	print(i)

# 	# Create JSON File with a project
# 	project_json = {}

# 	# Field - Name
# 	project_json["name"] = data.get("items")[i].get("name")

# 	# Field - Full Name
# 	project_json["full_name"] = data.get("items")[i].get("full_name")

# 	# Field - Owner Name
# 	project_json["owner_name"] = data.get("items")[i].get("owner").get("login")

# 	# Field - Repo HTML URL
# 	project_json["html_url"] = data.get("items")[i].get("html_url")

# 	# Field - Repo Description
# 	project_json["description"] = data.get("items")[i].get("description")

# 	# Field - Repo API URL for downloading
# 	project_json["api_url"] = data.get("items")[i].get("url")

# 	# Field - Created Time
# 	project_json["created_at"] = data.get("items")[i].get("created_at")

# 	# Field - Updated Time
# 	project_json["updated_at"] = data.get("items")[i].get("updated_at")

# 	# Field - Programming Language
# 	project_json["language"] = data.get("items")[i].get("language")

# 	# Field - Has Wiki
# 	project_json["has_wiki"] = data.get("items")[i].get("has_wiki")

# 	# Field - Source
# 	project_json["source"] = "github"

# 	print(json.dumps(project_json, indent = 2))

# 	# Config File Name
# 	project_filename = project_json["owner_name"] + "_" + project_json["name"]
# 	json_filename = project_filename + ".json"
# 	zip_filename = project_filename + ".zip"

# 	# Save the JSON file
# 	with open(os.path.join(output_dirname, json_filename), 'w') as file:
# 	    file.write(json.dumps(project_json, indent = 2))

# 	# Make a download request
# 	r = requests.get(project_json["api_url"] + "/zipball", auth = HTTPBasicAuth('SoapKe', 'BBC19951228Soap'))

# 	print(r.status_code)

# 	# Download the project
# 	with open(os.path.join(output_dirname, zip_filename), 'wb') as f:
# 		f.write(r.content)

##### Rate Limit Testing #####

# r = requests.get('https://api.github.com/rate_limit', auth=HTTPBasicAuth('SoapKe', 'BBC19951228Soap'))
# print(r.status_code)
# # print(json.loads(r.text))

# # json_rate = json.loads(r.text)

# print(json.dumps(r.json(), indent = 2))