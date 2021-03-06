from datetime import datetime
from fastapi import FastAPI, HTTPException
from http.client import HTTPException
from fastapi.staticfiles import StaticFiles

from uuid import uuid4
import random
import os
from datetime import datetime, timedelta
from pydantic import BaseModel
from data import User, Resource, get_last_update_db

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
        x = int(request["x"])
        y = int(request["y"])
        user.x += x
        user.y += y
        return { "x": user.x, "y": user.y }
    
@api.post("/users")
async def user_create(request: dict):
    x = random.randint(0, MAP_WIDTH)
    y = random.randint(0, MAP_HEIGHT)

    name = request["name"]

    user = User(name, x, y)
    users[user.uuid] = user
    return user

@api.get("/update/last")
async def get_last_update():
    return get_last_update_db()

app.mount("/api", api)
app.mount("/", StaticFiles(directory="static", html=True), name="static")


