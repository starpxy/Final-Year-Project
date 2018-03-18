# -*- coding: utf-8 -*-
""" 
@author:songhao 
@file: c4.py 
@time: 2017/12/19 
"""

import os
from urllib.request import urlopen

import requests
from tqdm import tqdm


def download_from_url(url, dst):
	"""
	@param: url to download file
	@param: dst place to put the file
	"""
	file_size = int(urlopen(url).info().get('Content-Length', -1))

	"""
	print(urlopen(url).info())
	# output
	Server: AliyunOSS
	Date: Tue, 19 Dec 2017 06:55:41 GMT
	Content-Type: application/octet-stream
	Content-Length: 29771146
	Connection: close
	x-oss-request-id: 5A38B7EDCE2B804FFB1FD51C
	Accept-Ranges: bytes
	ETag: "9AA9C1783224A1536D3F1E222C9C791B-6"
	Last-Modified: Wed, 15 Nov 2017 10:38:33 GMT
	x-oss-object-type: Multipart
	x-oss-hash-crc64ecma: 14897370096125855628
	x-oss-storage-class: Standard
	x-oss-server-time: 4
	"""

	if os.path.exists(dst):
		first_byte = os.path.getsize(dst)
	else:
		first_byte = 0
	if first_byte >= file_size:
		return file_size
	header = {"Range": "bytes=%s-%s" % (first_byte, file_size)}
	pbar = tqdm(
		total=file_size, initial=first_byte,
		unit='B', unit_scale=True, desc=url.split('/')[-1])
	req = requests.get(url, headers=header, stream=True)
	with(open(dst, 'ab')) as f:
		for chunk in req.iter_content(chunk_size=1024):
			if chunk:
				f.write(chunk)
				pbar.update(1024)
	pbar.close()
	return file_size


if __name__ == '__main__':
	url = "http://newoss.maiziedu.com/machinelearning/pythonrm/pythonrm5.mp4"
	download_from_url(url, "./new.mp4")