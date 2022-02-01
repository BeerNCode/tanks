from datetime import datetime
from fastapi import FastAPI, HTTPException
from http.client import HTTPException
from fastapi.staticfiles import StaticFiles
from azure.core.credentials import AzureNamedKeyCredential
from azure.data.tables import TableServiceClient
from uuid import uuid4
import random
import os
from datetime import datetime, timedelta
from pydantic import BaseModel

MAP_WIDTH = 100
MAP_HEIGHT = 100
NUMBER_OF_RESOURCES = 100
RESOURCE_TYPES = [
    "bullets",
    "health",
    "fuel"
]
DELTA = timedelta(60)

app = FastAPI()
api = FastAPI()

class User:
    def __init__(self, name, x, y):
        self.uuid = str(uuid4())
        self.name = name
        self.x = x
        self.y = y
        self.score = 0
        self.resources = {}

class Resource:
    def __init__(self, type, x, y):
        self.type = type
        self.x = x
        self.y = y

users = {}
resources = []
while len(resources) < NUMBER_OF_RESOURCES:
    x = random.randint(0, MAP_WIDTH)
    y = random.randint(0, MAP_HEIGHT)
    current = next((r for r in resources if r.x == x and r.y == y), None)
    if current is None:
        type = random.choice(RESOURCE_TYPES)
        resources.append(Resource(type, x, y))

@api.get("/map")
async def root():
    return { 
        "map_width": MAP_WIDTH,
        "map_height": MAP_HEIGHT,
        "resources": resources,
        "users": [{ "x": user.x, "y": user.y, "name": user.name } for user in users.values()]
    }

@api.get("/users")
async def get_users():
    return [{ "x": user.x, "y": user.y, "name": user.name } for user in users.values()]

@api.post("/users/{user_uuid}")
async def post_users(user_uuid, request: dict):
    if user_uuid not in users:
        raise HTTPException(status=400)
        
    user = users[user_uuid]
    command = request["command"]
    if command == "move":
        x = int(command["x"])
        y = int(command["y"])
        user.x += x
        user.y += y
    
@api.get("/users/create")
async def user_create(name):
    x = random.randint(0, MAP_WIDTH)
    y = random.randint(0, MAP_HEIGHT)

    user = User(name, x, y)
    users[user.uuid] = user
    return user

@api.get("/update/last")
async def get_last_update():
    return get_last_update_db()

app.mount("/api", api)
app.mount("/", StaticFiles(directory="static", html=True), name="static")

def get_last_update_db():
    try:
        STORAGE_KEY = os.getenv('STORAGE_KEY')
        credential = AzureNamedKeyCredential("tanks", STORAGE_KEY)
        service = TableServiceClient(endpoint="https://tanks.table.core.windows.net", credential=credential)
        table_name = "updatetime"
        service.create_table_if_not_exists(table_name=table_name)
        table = service.get_table_client(table_name=table_name)
        try:
            entities = table.query_entities("PartitionKey eq 'Time'")
            current = entities.next()
        except:
            print("AAAAAA")
        if current is None:
            table.create_entity({
                u'PartitionKey': "Time",
                u'RowKey': "Time",
                u'LastUpdate': datetime.now()
            })
        else:
            table.update_entity({
                u'PartitionKey': "Time",
                u'RowKey': "Time",
                u'LastUpdate': datetime.now()
            })
        return current
    except:
        return "Cannot get last update"
