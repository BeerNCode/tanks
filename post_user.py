import requests

API_URL = "https://fnc-tanks.azurewebsites.net/api"
USER_UUID = "d389df1a-5a3b-4da6-a9d2-8064bcfb7395"

print(API_URL + f"/users/{USER_UUID}")
response = requests.post(API_URL + f"/users/{USER_UUID}", json={
    "command": "move"
})
print(response)