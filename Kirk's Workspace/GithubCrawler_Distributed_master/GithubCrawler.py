import os
import io
import sys
import json
import time
import zipfile

import requests
from requests.auth import HTTPBasicAuth

from tqdm import tqdm

from DF.core.Client import Client

from LogWriter import LogWriter


class GithubCrawler(object):
	"""docstring for GithubCrawler"""
	def __init__(self):
		super(GithubCrawler, self).__init__()
		self.log_writer = LogWriter()

		# Change Account ?
		self.g_account = None

		self.next_search_page = None
		self.next_search_stars_ub = None
		self.download_record_filepath = ""
		self.output_path = "python"

	def config_github_account(self, username, password):
		self.g_account = HTTPBasicAuth(username, password)

	def call_api_search(self, language, stars_ub = ""):
		# Check Github Account Rate Limit
		if self.check_api_ratelimit():
			if(self.next_search_page == None):
				# Logging
				self.log_writer.write_info_log("Call Github API Search")

				'''
					With Request Lib
				'''  

				# Create params for Github Search API
				if(stars_ub == ""):
					payload = {
						"q": "language:" + language,
						"sort": "stars",
						"order": "desc",
						"per_page": "100"
					}
				else:
					payload = {
					"q": "language:" + language + " " + "stars:<=" + str(stars_ub),
					"sort": "stars",
					"order": "desc",
					"per_page": "100"
				}

				# Call Github Search API
				response = requests.get(
					"https://api.github.com/search/repositories", 
					params = payload,
					auth = self.g_account
					)

				print(response.url)

				self.next_search_page = response.links.get("next").get("url")

				print(response.links.get("next"))

				# Logging
				self.log_writer.write_info_log("Call Github API Search is done")

				return response.json()

			else:
				# Call Github Search API
				response = requests.get(
					self.next_search_page,
					auth = self.g_account
					)


				
				# If it is not the last page
				if(response.links.get("next") != None):
					self.next_search_page = response.links.get("next").get("url")

					print(response.links.get("next"))

				
				# If it is the last page
				else:
					# Set [Next Page] to [None] for the next range of search
					self.next_search_page = None

					# Record the stars count of the last repo
					next_tmp = response.json().get("items")[-1].get("stargazers_count")

					# To see: Have reached the API Search Limitation?
					if(next_tmp != self.next_search_stars_ub):
						self.next_search_stars_ub = response.json().get("items")[-1].get("stargazers_count")
					else:
						print(self.next_search_stars_ub)
						print("Reach the limitation")

						# Set a flag to stop crawling
						self.next_search_page = "END"

				return response.json()
		else:
			self.log_writer.write_error_log("call_api_search failed")
			pass

	def check_api_ratelimit(self):
		# Config Github Account

		api_rate_limit = "https://api.github.com/rate_limit" 

		try:
			response = requests.get(url = api_rate_limit, timeout= 15.5, auth = self.g_account)

		except requests.exceptions.Timeout:
			self.log_writer.write_error_log("Download request ---- TIMEOUT" + " url: " + download_url)
			
			# TO DO: Reconnect
			self.check_api_ratelimit()

		except requests.exceptions.HTTPError:
			self.log_writer.write_error_log("Download request ---- BAD REQUEST " + "HTTP Response Status Code: " + str(response.status_code) + " url: " + download_url)

			# TO DO: Reconnect
			self.check_api_ratelimit()

		else:
			print(response.status_code)
			print(response.json().get("resources").get("search"))

			# Get remaning number of times for Search API Request
			remaining_times = response.json().get("resources").get("search").get("remaining")

			# Get API rate limit reset time -- in Unix Time
			reset_time = response.json().get("resources").get("search").get("reset")
			
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

	def save_repo_info_to_json(self, api_json):
		# Create JSON 
		repo_json = {}

		# Store Field -- Repo Name
		repo_json["name"] = api_json.get("name")

		# Store Field -- Repo Full Name
		repo_json["full_name"] = api_json.get("full_name")

		# Store Field -- Repo Owner Name
		repo_json["owner_name"] = api_json.get("owner").get("login")

		# Store Field -- Repo HTML URL
		repo_json["html_url"] = api_json.get("html_url")

		# Store Field -- Repo Description
		repo_json["description"] = api_json.get("description")

		# Store Field -- Repo Api URL for downloading
		repo_json["api_url"] = api_json.get("url")

		# Store Field -- Repo Created Time
		repo_json["created_at"] = api_json.get("created_at")

		# Store Field -- Repo Updated Time
		repo_json["updated_at"] = api_json.get("updated_at")

		# Store Field -- Repo Programming Language
		repo_json["language"] = api_json.get("language")

		# Store Field -- Repo Has Wiki
		repo_json["has_wiki"] = api_json.get("has_wiki")

		# Store Field -- Source
		repo_json["source"] = "github"

		# Save to JSON file
		repo_name = repo_json["full_name"].replace("/", "-")

		with open(os.path.join(self.output_path, repo_name) + ".json", "w") as file:
			file.write(json.dumps(repo_json, indent = 2))

	def download(self, download_url, download_filename):
		### Download does not cost the API Times ###

		# Authentication?
		# Header -- if need?

		# Handle [timeout] & [stream transmission]
		'''
			HTTP Request to download the repo
			Handle all the excepotions
		'''
		try:
			headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
			'Accept-Encoding': 'identity'
			}

			response = requests.get(download_url + "/zipball", headers = headers, timeout= 15.5, stream = True,  auth = self.g_account)
		
		except requests.exceptions.Timeout:
			# Logging
			self.log_writer.write_error_log("Download request ---- TIMEOUT" + " url: " + download_url)

			# Formatting
			print("")

			# TO DO: Reconnect
			self.download(download_url, download_filename)

		except requests.exceptions.HTTPError:
			# Logging
			self.log_writer.write_error_log("Download request ---- BAD REQUEST " + "HTTP Response Status Code: " + str(response.status_code) + " url: " + download_url)

			# Formatting
			print("")

			# TO DO: Reconnect
			self.download(download_url, download_filename)

		except requests.exceptions.ConnectionError:
			# Logging
			self.log_writer.write_error_log("Download request ---- Connection broken due to bad Internet condition" + " url: " + download_url)

			# Formatting
			print("")

			# TO DO: Reconnect
			self.download(download_url, download_filename)		

		else:
			'''
				Get the size of the repo
				Star to download
				Handle all the excepotions
			'''

			# Content length -- Chunked
			file_size = response.headers.get("content-length")

			if file_size != None:				
				# Unit in byte
				pbar = tqdm(total = int(file_size), ncols = 80, ascii = False, unit = 'b', unit_scale = True, desc = download_filename)

			else:
				# Unit in byte
				pbar = tqdm(total = None, ncols = 80, ascii = False, unit = 'b', unit_scale = True, desc = download_filename)

			# Have a chance to fail, when the Internet Connection is bad
			try:
				with open(os.path.join(self.output_path, download_filename) + ".zip", "wb") as f:
					# Chunk size unit in byte
					for chunk in response.iter_content(chunk_size = 1024): 
						if chunk:
							f.write(chunk)
							pbar.update(1024)

				# Test the integrity of .Zip files
				with zipfile.ZipFile(os.path.join(self.output_path, download_filename) + ".zip", 'r') as zipfile_test:
					zipfile_test.testzip()

				# Logging
				self.log_writer.write_info_log("Download request ---- Download Complete! Zip file is fine!" + " url: " + download_url)

			except requests.exceptions.ConnectionError:
				# Logging
				self.log_writer.write_error_log("Download request ---- Connection broken due to bad Internet condition" + " url: " + download_url)

				# Close the Progress Bar
				pbar.close()

				# Close the request
				response.close()

				# Formatting
				print("")

				# TO DO: Reconnect
				self.download(download_url, download_filename)

			except requests.exceptions.ChunkedEncodingError:
				self.log_writer.write_error_log("Download request ---- Connection broken due to bad Internet condition" + " url: " + download_url)

				# Close the Progress Bar
				pbar.close()

				# Close the request
				response.close()

				# Formatting
				print("")

				# TO DO: Reconnect
				self.download(download_url, download_filename)

			except zipfile.BadZipFile:
				# Test
				# print("zipfile is broken: " + download_filename)

				# Log
				self.log_writer.write_error_log("Download request ---- Zip file broken" + " url: " + download_url)

				# Close the Progress Bar
				pbar.close()

				# Close the request
				response.close()

				# Formatting
				print("")

				# TO DO: Reconnect
				self.download(download_url, download_filename)

			finally:
				# Close the Progress Bar
				pbar.close()

				# Close the request
				response.close()

				# Formatting
				print("")

	def check_repo_records(self, api_json):
		# repo id
		repo_id = str(api_json.get("id"))


		'''
			Read the Download_Recrod from json
		'''

		# If the Download_Record File doesn't exsit, then create it
		if not(os.path.exists(self.download_record_filepath) and os.path.isfile(self.download_record_filepath)):
			# Logging
			self.log_writer.write_error_log("Download_Record Json File doesn't exist")

			# Create the Download_Record Json File when it is the first time to run
			with open(self.download_record_filepath, 'w') as f:
				return True
		else:
			with open(self.download_record_filepath, 'r') as f:
				if not f.read() == "":
					download_info_json = json.load(f)
				else:
					return True

		'''
			Check the repo has been downloaded or not
		'''

		# If the repo has been downloaded
		if(download_info_json.get(repo_id) != None):
			'''
				Check and Update the stars
			

			# Old stars
			old_stars = download_info_json.get(repo_id).get("stars")
			print(old_stars)

			# New stars
			new_stars = api_json.get("stargazers_count")
			print(new_stars)


			if(old_stars != new_stars):
				# Prompt
				print("Star changes")

				# Record the new stars
				download_info_json[repo_id]["stars"] = new_stars
				
				# Update the downloaded repo info in the Download_Record Json File
				with open(self.download_record_filepath, 'w') as f:
					f.write(json.dumps(download_info_json, indent = 2))
			
			'''

			'''
				Check and Update the repo
				Whether the repo has been updated after last time we downloaded it
			'''

			# Old updated time
			old_updated = download_info_json.get(repo_id).get("updated_at")
			print(old_updated)


			# New updated time
			new_updated = api_json.get("updated_at")
			print(new_updated)

			if(old_updated != new_updated):
				# Prompt
				print("Repo Updated")

				# Record the new updated time
				download_info_json[repo_id]["updated_at"] = new_updated

				# Update the downloaded repo info in the Download_Record Json File
				with open(self.download_record_filepath, 'w') as f:
					f.write(json.dumps(download_info_json, indent = 2))

				# Logging
				self.log_writer.write_info_log("Check repo records ---- Repo need to update." + " url: " + api_json.get("url"))

				# Need update -- repo has been updated
				return True

			else:
				# Logging
				self.log_writer.write_info_log("Check repo records ---- Repo does not need to update." + " url: " + api_json.get("url"))

				# don't need update -- repo has not been updated
				return False

		# If it is a new repo
		else:
			# Logging
			self.log_writer.write_info_log("Check repo records ---- Repo is new! Need to be downloaded." + " url: " + api_json.get("url"))

			# Need download
			return True

	def save_download_info_to_json(self, api_json):
		'''
			Read the Download_Recrod from json
		'''

		# If the Download_Record File doesn't exsit, then create it
		if not(os.path.exists(self.download_record_filepath) and os.path.isfile(self.download_record_filepath)):
			with open(self.download_record_filepath, 'w') as f:
				pass
		else:
			with open(self.download_record_filepath, 'r') as f:
				download_record_json = json.load(f)

		# Create Repo info dict
		repo_info = {}

		# Store Field -- Repo Updated time
		repo_info["updated_at"] = api_json.get("updated_at")

		# Store Field -- Repo Updated time
		repo_info["stars"] = api_json.get("stargazers_count")

		# Store Field -- Repo ID
		download_record_json[api_json.get("id")] = repo_info

		# Save to json file
		with open("download_records_test" + ".json", "w") as f:
			f.write(json.dumps(download_record_json, indent = 2))

def main():
	# Configs
	language = "java"
	output_path = os.path.join("home", "ubuntu", "github_repo", language)
	stop_nums = 300

	crawler = GithubCrawler()
	crawler.config_github_account("SoapKe", "BBC19951228Soap")

	# Config the output path
	if not os.path.exists(output_path):
		os.mkdir(output_path)

	crawler.output_path = output_path

	# Config the download_records file path
	if not os.path.exists("data"):
		os.mkdir("data")

	crawler.download_record_filepath = os.path.join("data", "github_repo_records_" + language + ".json")

	total = 0

	# local master machine task list
	local_repo_list = []

	# Keep assigning tasks
	while True:
		if(crawler.next_search_stars_ub == None):
			data = crawler.call_api_search(language)
		else:
			data = crawler.call_api_search(language, crawler.next_search_stars_ub)

		repo_json_list = data.get("items")

		# Assign tasks to slave servers
		if( (total % 300) == 0):
			# DF
			client = Client("172.21.0.2", 9002)
			client.send_message(repo_json_list)
		elif( (total % 300) == 100):
			# DF
			client = Client("172.21.0.11", 9002)
			client.send_message(repo_json_list)
		elif( (total % 300) == 200):
			# Add it to local task list
			local_repo_list = local_repo_list + repo_json_list


		total += len(data.get("items"))
		print(total)

		if(crawler.next_search_page == "END"):
			break
		elif(total == stop_nums):
			break

	# Start local tasks
	
	# For each repo in the json result
	for i in range(len(local_repo_list)):
		# Check if it has been downloaded already
		if(crawler.check_repo_records(local_repo_list[i])):

			# Save repo json
			crawler.save_repo_info_to_json(local_repo_list[i])

			# Download repo
			crawler.download(local_repo_list[i].get("url"), local_repo_list[i].get("full_name").replace("/", "-"))

			# Save download info to json
			crawler.save_download_info_to_json(local_repo_list[i])

if __name__ == '__main__':
	main()