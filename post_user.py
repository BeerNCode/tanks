import requests

API_URL = "https://fnc-tanks.azurewebsites.net/api"
# API_URL = "http://localhost:8000/api"
USER_UUID = "dabb5894-7855-4b3a-b405-8432d0aa7d32"

print(API_URL + f"/users/{USER_UUID}")
response = requests.post(API_URL + f"/users/{USER_UUID}", json={
    "command": "move",
    "x" : 10,
    "y": 1
})
print(response)