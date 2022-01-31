import requests

API_URL = "https://fnc-tanks.azurewebsites.net/api"
# API_URL = "http://localhost:8000/api"
USER_UUID = "697d5419-d02d-4da3-8ca9-b454833bba9d"

print(API_URL + f"/users/{USER_UUID}")
response = requests.post(API_URL + f"/users/{USER_UUID}", json={
    "command": "move",
    "x" : 10,
    "y": 1
})
print(response)