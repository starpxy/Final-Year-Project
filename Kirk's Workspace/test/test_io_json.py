import os
import json

# Download_Record File Name
download_record_filename = "test_io.json"

# Read the Download_Recrod from json
if not( os.path.exists(download_record_filename) and os.path.isfile(download_record_filename) ):
	with open(download_record_filename, 'w') as f:
		pass
