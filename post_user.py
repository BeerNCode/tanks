import requests

# API_URL = "https://fnc-tanks.azurewebsites.net/api"
API_URL = "http://localhost:8000/api"

response = requests.post(API_URL + f"/users", json={
    "name": "Tom"
})
data = response.json()
print(data)
user_uuid = data["uuid"]

command_url = API_URL + f"/users/{user_uuid}"


response = requests.post(command_url, json={
    "command": "move",
    "x" : 10,
    "y": 1
})
print(response)
print(response.text)