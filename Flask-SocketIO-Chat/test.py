import requests
import json

URL = "http://127.0.0.1:5000//getChat"

for i in range(1000): 
    # sending get request and saving the response as response object
    r = requests.get(url = URL)
    data = r.json()
    print(data)

  
