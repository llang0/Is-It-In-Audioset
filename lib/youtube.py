# get youtube title

import requests
import json
import urllib

ytid = "NGX1CNIV8_g"

params = {"format": "json", "url": f"https://www.youtube.com/watch?v={ytid}"}

url = "https://www.youtube.com/oembed"
query_string = urllib.parse.urlencode(params)
url = url + "?" + query_string

response = requests.get(url)
data = response.json()

print(data["title"])