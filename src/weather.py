import json

import requests

from config import url

response = requests.get(url)

with open('weather.json', 'w') as f:
    f.write(json.dumps(response.json()))
