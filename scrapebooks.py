#!/usr/bin/python3

import sys
import re
import requests
import argparse
from threading import Thread

parser = argparse.ArgumentParser()
parser.add_argument("query",nargs='+')
parser.add_argument("-n",type=int,default=10)
args = parser.parse_args()

def download_file(url,filename):
	try:
		with requests.get(url) as r:
			with open(filename, 'wb') as f:
				for chunk in r.iter_content(chunk_size=128):
					f.write(chunk)
		print(f"Finished downloading {filename} from {url}")
	except Exception as e:
		print(e)
threads = []

regex = r"[\w\W]+\&(.+)';\nuxrl=uxrl\+'(.+)';[\w\W]+"

params = {
	"format"		: "json",
	"q"			: ' '.join(args.query), # query
	"c"			: "main", # content
	"filetype"		: "pdf",
	"n"			: args.n, # number of results
}

with requests.get("http://gigablast.com/search",params=params) as r:
	# Gigablast has this weird thing where it adds a ramdom value to the link before it works
	key, value = re.sub(regex,r"\1\2",r.text).split('=')
	params[key] = value

with requests.get("http://gigablast.com/search",params=params) as r:
		response_dict = r.json()

n = 0

for result in response_dict["results"]:
	url = result["url"]
	title = result["title"]
	filename = url.split('/')[-1]
	threads.append(Thread(
			target=download_file,
			args=(url,f"{n}.pdf")
				)
			)
	n += 1

for thread in threads:
	thread.start()
