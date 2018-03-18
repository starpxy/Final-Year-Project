import os
import io
import sys
import json
import time

import requests
from requests.auth import HTTPBasicAuth

from agithub.GitHub import GitHub

from tqdm import tqdm

from LogWriter import LogWriter

class GithubCrawler(object):
	"""docstring for GithubCrawler"""
	def __init__(self):
		super(GithubCrawler, self).__init__()
		self.log_writer = LogWriter()

		# Change Account ?
		# self.g = GitHub("SoapKe", "BBC19951228Soap") # Config Github Account

		self.g = GitHub("", "")

		self.output_path = "python\\"

	def config_github_account(self, username, password):
		self.g = GitHub(username, password)
		# return g

	def call_api_search(self, account, language, page, per_page):
		# Check Github Account Rate Limit
		if self.check_api_ratelimit(account):
			g = account
			status, data = g.search.repositories.get(
				q = "language:" + language,
				sort = "stars",
				order = "desc",
				page = page,
				per_page = per_page
				)
			return status, data
		else:
			self.log_writer.write_error_log("call_api_search failed")
			pass

	def check_api_ratelimit(self, account):
		# Config Github Account
		g = account

		status, data = g.rate_limit.get()

		print(status)
		print(json.dumps(data, indent = 2))

		# Get remaning number of times for Search API Request
		remaining_times = data.get("resources").get("search").get("remaining")

		# Get API rate limit reset time -- in Unix Time
		reset_time = data.get("resources").get("search").get("reset")
		
		if remaining_times > 0:
			return True
		else:
			# Get current sys time in Unix Time
			current_time = int(time.time())

			# Get wait time
			wait_time = reset_time - current_time

			# Log
			self.log_writer.write_info_log("Wait for API rate limit reset. Thread sleep for " + str(wait_time) + " seconds")

			# Test
			print("Wait for API reset" + str(wait_time) + " seconds")

			# Hold the theard
			time.sleep(wait_time)

			# Check again
			self.check_api_ratelimit()

	def save_project_info_to_json(self, api_json):
		# Create JSON 
		project_json = {}

		# Store Field -- Repo Name
		project_json["name"] = api_json.get("name")

		# Store Field -- Repo Full Name
		project_json["full_name"] = api_json.get("full_name")

		# Store Field -- Repo Owner Name
		project_json["owner_name"] = api_json.get("owner").get("login")

		# Store Field -- Repo HTML URL
		project_json["html_url"] = api_json.get("html_url")

		# Store Field -- Repo Description
		project_json["description"] = api_json.get("description")

		# Store Field -- Repo Api URL for downloading
		project_json["api_url"] = api_json.get("url")

		# Store Field -- Repo Created Time
		project_json["created_at"] = api_json.get("created_at")

		# Store Field -- Repo Updated Time
		project_json["updated_at"] = api_json.get("updated_at")

		# Store Field -- Repo Programming Language
		project_json["language"] = api_json.get("language")

		# Store Field -- Repo Has Wiki
		project_json["has_wiki"] = api_json.get("has_wiki")

		# Store Field -- Source
		project_json["source"] = "github"

		# Save to JSON file
		project_name = project_json["full_name"].replace("/", "-")

		with open(self.output_path + project_name + ".json", "w") as file:
			file.write(json.dumps(project_json, indent = 2))

	def download(self, download_url, download_filename):
		### Download does not cost the API Times ###

		# Authentication?
		# Header -- if need?

		# Handle [timeout] & [stream transmission]
		try:
			response = requests.get(download_url + "/zipball", timeout=(3.05, 27), stream = True,  auth = HTTPBasicAuth('SoapKe', 'BBC19951228Soap'))
		except Timeout:
			self.log_writer.write_error_log("Download request ---- TIMEOUT")
			
			# TO DO: Reconnect

		except HTTPError:
			self.log_writer.write_error_log("Download request ---- BAD REQUEST " + "HTTP Response Status Code: " + str(response.status_code))

			# TO DO: Reconnect

		else:
			# Content length -- Chunked
			##### TO DO #####
			file_size = response.headers.get("content-length")
			print(file_size)

			if file_size != None:				
				# Unit in byte
				pbar = tqdm(total = int(file_size), ncols = 80, ascii = False, unit = 'b', unit_scale = True, desc = download_filename)

			else:
				# Unit in byte
				pbar = tqdm(total = None, ncols = 80, ascii = False, unit = 'b', unit_scale = True, desc = download_filename)

			# Have a chance to fail, when the Internet Connection is bad
			# Retry? How to catch breakconnection when "stream = True"
			# ----> Solution: Just download first, and check the file integrity when Ciaran unzip the files
			with open(self.output_path + download_filename + ".zip", "wb") as f:
				# Chunk size unit in byte
				for chunk in response.iter_content(chunk_size = 1024): 
					if chunk:
						f.write(chunk)
						pbar.update(1024)

			# Close the Progress Bar
			pbar.close()
			# Close the request
			response.close()

	def run(self):
		pass


def main():

	crawler = GithubCrawler()
	crawler.config_github_account("SoapKe", "BBC19951228Soap")
	status, data = crawler.call_api_search(crawler.g, "python", "1", "100")

	# print(json.dumps(data, indent = 2))

	project_json_list = data.get("items")

	# For each project in the json result
	for i in range(len(project_json_list)):
		# Check if it has been downloaded already
		##### TO DO #####

		# Save project json
		crawler.save_project_info_to_json(project_json_list[i])

		# Download project
		crawler.download(project_json_list[i].get("url"), project_json_list[i].get("full_name").replace("/", "-"))


	# crawler.check_api_ratelimit()

if __name__ == '__main__':
	main()