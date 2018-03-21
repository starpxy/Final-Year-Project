import os
import io
import sys
import json
import time
import zipfile

import requests
from requests.auth import HTTPBasicAuth

from tqdm import tqdm

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
		self.output_path = "..\\..\\python"

	def config_github_account(self, username, password):
		self.g_account = HTTPBasicAuth(username, password)


	def call_api_search(self, language, stars_ub = ""):
		# Check Github Account Rate Limit
		if self.check_api_ratelimit():
			if(self.next_search_page == None):
				# g = account

				# # Test for agithub moudle
				# self.log_writer.write_info_log("Call agithub Search")

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
					auth = HTTPBasicAuth('SoapKe', 'BBC19951228Soap')
					)

				print(response.url)

				self.next_search_page = response.links.get("next").get("url")

				# if(response.links.get("next") != None):
				# 	self.next_search_page = response.links.get("next").get("url")

				# 	# Set [Next Page] to [None] for the next range of search
				# 	self.next_search_stars_ub = None	
				# else:
				# 	# Record the stars count of the last repo
				# 	self.next_search_stars_ub = response.json().get("items")[-1].get("stargazers_count")

				# 	# Set [Next Page] to [None] for the next range of search
				# 	self.next_search_page = None

				# print(response.links["next"])
				print(response.links.get("next"))

				return response.json()

				# # Test for agithub moudle
				# self.log_writer.write_info_log("Call agithub Search had done")

			else:
				# Call Github Search API
				response = requests.get(
					self.next_search_page,
					auth = HTTPBasicAuth('SoapKe', 'BBC19951228Soap')
					)

				'''
				If it is not the last page
				'''
				if(response.links.get("next") != None):
					self.next_search_page = response.links.get("next").get("url")

					print(response.links.get("next"))
				
				# If it is the last page
				else:
					# Record the stars count of the last repo
					next_tmp = response.json().get("items")[-1].get("stargazers_count")

					if(next_tmp != self.next_search_stars_ub):
						self.next_search_stars_ub = response.json().get("items")[-1].get("stargazers_count")
					else:
						print(self.next_search_stars_ub)
						print("Reach the limitation")

						# Set a flag to stop crawling
						self.next_search_page = "END"

						return response.json()

						
					# Set [Next Page] to [None] for the next range of search
					self.next_search_page = None

				return response.json()
		else:
			self.log_writer.write_error_log("call_api_search failed")
			pass

	def check_api_ratelimit(self):
		# Config Github Account

		api_rate_limit = "https://api.github.com/rate_limit" 

		try:
			response = requests.get(url = api_rate_limit, auth = self.g_account)

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
		try:
			headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
			'Accept-Encoding': 'identity'
			}

			response = requests.get(download_url + "/zipball", headers = headers, timeout= 15.5, stream = True,  auth = HTTPBasicAuth('SoapKe', 'BBC19951228Soap'))
		except requests.exceptions.Timeout:
			self.log_writer.write_error_log("Download request ---- TIMEOUT" + " url: " + download_url)
			
			# TO DO: Reconnect
			self.download(download_url, download_filename)

		except requests.exceptions.HTTPError:
			self.log_writer.write_error_log("Download request ---- BAD REQUEST " + "HTTP Response Status Code: " + str(response.status_code) + " url: " + download_url)

			# TO DO: Reconnect
			self.download(download_url, download_filename)

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

			try:
				with open(os.path.join(self.output_path, download_filename) + ".zip", "wb") as f:
					# Chunk size unit in byte
					for chunk in response.iter_content(chunk_size = 1024): 
						if chunk:
							f.write(chunk)
							pbar.update(1024)

				# ZIP File integrity test
				# Test
				# print("zipfile test begin: " + download_filename)

				with zipfile.ZipFile(os.path.join(self.output_path, download_filename) + ".zip", 'r') as zipfile_test:
					zipfile_test.testzip()

				# Log
				self.log_writer.write_info_log("Download request ---- Complete! Zip file fine!" + " url: " + download_url)

				# Test
				# print("zipfile is fine: " + download_filename)

			except requests.exceptions.ConnectionError:
				self.log_writer.write_error_log("Download request ---- Connection broken due to bad Internet condition" + " url: " + download_url)
				
				# TO DO: Reconnect
				self.download(download_url, download_filename)

			except requests.exceptions.ChunkedEncodingError:
				self.log_writer.write_error_log("Download request ---- Connection broken due to bad Internet condition" + " url: " + download_url)
			
				# TO DO: Reconnect
				self.download(download_url, download_filename)

			except zipfile.BadZipFile:
				# Test
				# print("zipfile is broken: " + download_filename)

				# Log
				self.log_writer.write_error_log("Download request ---- Zip file broken" + " url: " + download_url)

				# TO DO: Reconnect
				self.download(download_url, download_filename)

			finally:
				# Close the Progress Bar
				pbar.close()
				# Close the request
				response.close()

				# Record the info in database or just json file by now
				# repo id / downloaded time / updated time / stars

				print("")

	def check_repo_records(self, api_json):
		# repo id
		repo_id = str(api_json.get("id"))

		try:
			with open("download_records_test" + ".json", "r") as file:
				download_info_json = json.load(file)
		except Exception as e:
			# Handle none file exception
			raise
		else:
			# old repo
			# print(download_info_json.get(repo_id))

			if(download_info_json.get(repo_id) != None):
				# Check and update the stars
				# Update the stars
				print(download_info_json.get(repo_id).get("stars"))
				print(api_json.get("stargazers_count"))

				if(download_info_json.get(repo_id).get("stars") != api_json.get("stargazers_count")):
					download_info_json[repo_id]["stars"] = api_json.get("stargazers_count")
					print("Star changes")
				# Pass
				else:
					pass

				# If the repo has been updated after last time we downloaded it
				if(download_info_json.get(repo_id).get("updated_at") != api_json.get("updated_at")):
					print(download_info_json.get(repo_id).get("updated_at"))
					print(api_json.get("updated_at"))

					# need update -- repo has been updated
					return True

				else:
					# don't need update --repo has not been updated
					return False

			# new repo
			else:
				# need download
				return True

	def save_download_info_to_json(self, api_json):
		# Open the download records
		try:
			with open("download_records_test" + ".json", "r") as file:
				download_record_json = json.load(file)
		except Exception as e:
			# Handle none file exception
			raise

		# Create Repo info dict
		repo_info = {}

		# Store Field -- Repo Updated time
		repo_info["updated_at"] = api_json.get("updated_at")

		# Store Field -- Repo Updated time
		repo_info["stars"] = api_json.get("stargazers_count")

		# Store Field -- Repo ID
		download_record_json[api_json.get("id")] = repo_info

		# Save to json file
		with open("download_records_test" + ".json", "w") as file:
			file.write(json.dumps(download_record_json, indent = 2))

	def run(self):
		pass

def main():

	crawler = GithubCrawler()
	crawler.config_github_account("SoapKe", "BBC19951228Soap")

	total = 0

	while True:
		if(crawler.next_search_stars_ub == None):
			data = crawler.call_api_search("python")
		else:
			data = crawler.call_api_search("python", crawler.next_search_stars_ub)

		repo_json_list = data.get("items")

		# For each repo in the json result
		for i in range(len(repo_json_list)):
			# Check if it has been downloaded already
			if(crawler.check_repo_records(repo_json_list[i])):

				# Save repo json
				crawler.save_repo_info_to_json(repo_json_list[i])

				# Download repo
				# crawler.download(repo_json_list[i].get("url"), repo_json_list[i].get("full_name").replace("/", "-"))

				# Save download info to json
				crawler.save_download_info_to_json(repo_json_list[i])

		if(crawler.next_search_page == "END"):
			exit()


		total += len(data.get("items"))
		print(total)

if __name__ == '__main__':
	main()