from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from uuid import uuid4
import random

MAP_WIDTH = 100
MAP_HEIGHT = 100

app = FastAPI()
api = FastAPI()

class User:
    def __init__(self, name, x, y):
        self.uuid = str(uuid4())
        self.name = name
        self.x = x
        self.y = y

users = {}

@api.get("/map")
async def root():
    return { 
        "map_width": MAP_WIDTH,
        "map_height": MAP_HEIGHT,
        "resources": [],
        "users": [{ "x": user.x, "y": user.y, "name": user.name } for user in users.values()]
    }

@api.get("/users")
async def get_users():
    return [{ "x": user.x, "y": user.y, "name": user.name } for user in users.values()]

@api.post("/users")
async def users_post():
    return "post"

@api.get("/users/create")
async def user_create(name):
    x = random.randint(0, MAP_WIDTH)
    y = random.randint(0, MAP_HEIGHT)

    user = User(name, x, y)
    users[user.uuid] = user
    return user

app.mount("/api", api)
app.mount("/", StaticFiles(directory="static"), name="static")