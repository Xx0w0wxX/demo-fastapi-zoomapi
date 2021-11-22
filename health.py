

import json
import requests
from pprint import pprint

f = open('credential.json')
credential = json.load(f)
f.close()

access_token = credential['access_token']

headers = {
    "Authorization": "Bearer {}".format(access_token)
}

url = "https://api.zoom.us/v2/users/me"
res = requests.get(url, headers=headers)

pprint(res.json())
