# coding=utf-8
# author:star
from DF.LogWriter import LogWriter
from GithubCrawler import GithubCrawler

class Task:
	__data = {}

	def __init__(self, data):
		self.__data = data

	#   TODO: Insert your task content here...
	def run(self):
		LogWriter().write_info_log("Running server task...")
		
		# Configs
		language = "java"
		output_path = os.path.join("home", "ubuntu", "github_repo", language)

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

		for i in range(len(self.__data)):
			# Check if it has been downloaded already
			if(crawler.check_repo_records(self.__data[i])):

				# Save repo json
				crawler.save_repo_info_to_json(self.__data[i])

				# Download repo
				crawler.download(self.__data[i].get("url"), self.__data[i].get("full_name").replace("/", "-"))

				# Save download info to json
				crawler.save_download_info_to_json(self.__data[i])