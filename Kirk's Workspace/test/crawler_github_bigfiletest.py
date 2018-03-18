import requests
from requests.auth import HTTPBasicAuth

import json
from agithub.GitHub import GitHub

import urllib.parse

import io
import os
import sys
import re
import http

# Store where?
from LogWriter import LogWriter

lg = LogWriter()

import urllib.request

# import http

# http.client.HTTPConnection._http_vsn = 10
# http.client.HTTPConnection._http_vsn_str = 'HTTP/1.0'

# File Path
dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))

print ("running from", dirname)
print ("file is", filename)

output_dirname = dirname + "\\python"

# Encode Config
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

# # Make a download request
# try:
# 	response = urllib.request.urlopen("https://api.github.com/repos/tensorflow/models" + "/zipball")
# 	print(type(response))

# 	project_data = b""
# 	while True:
# 		try:
# 			print("try")
# 			project_data_part = response.read()
# 		except http.client.IncompleteRead as icread:
# 			project_data = project_data + icread.partial
# 			print("Connection Break")
# 			continue
# 		else:
# 			print("else")
# 			project_data = project_data + project_data_part
# 			break

# 	with open(os.path.join(output_dirname, "bigfile.zip"), 'wb') as f:
# 		f.write(project_data)

# except Exception as RESTex:
# 	print("Exception occurred making REST call: " + RESTex.__str__())

# try:
# 	r = requests.get("https://api.github.com/repos/tensorflow/models" + "/zipball", auth = HTTPBasicAuth('SoapKe', 'BBC19951228Soap'))
# except (requests.exceptions.ChunkedEncodingError, requests.ConnectionError) as e:
# 	print("exception")

# 	lg.write_error_log("requests.exceptions.ChunkedEncodingError - Connection broken: IncompleteRead")

# # print(r.status_code)
# # print(type(r.status_code), r.status_code)
# # print(type(r.headers), r.headers)
# # print(type(r.cookies), r.cookies)
# # print(type(r.url), r.url)
# # print(type(r.history), r.history)

# # Download the project
# with open(os.path.join(output_dirname, "bigfile.zip"), 'wb') as f:
# 	f.write(r.content)

# Breakpoint Continuingly 


headers = {
	'Range': 'bytes=0-4'
}
https://api.github.com/repos/tensorflow/models/zipball
try:
	r = requests.head("https://api.github.com/repos/tensorflow/models" + "/zipball", headers = headers)
	# crange = r.headers['content-range']
	print(r.headers)
	# self.total = int(re.match(ur'^bytes 0-4/(\d+)$', crange).group(1))
except:
	pass

try:
	total = int(r.headers['content-length'])  
except:
	total = 0

print(total)

##### Rate Limit Testing #####

# r = requests.get('https://api.github.com/rate_limit', auth=HTTPBasicAuth('SoapKe', 'BBC19951228Soap'))
# print(r.status_code)
# print(json.loads(r.text))

# json_rate = json.loads(r.text)

# print(json.dumps(r.json(), indent = 2))