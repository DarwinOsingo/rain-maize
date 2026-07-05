##prog.py 
from pydantic import BaseModel
from fastapi import FastAPI,APIRouter 
from uuid import uuid4
import json
import os

router = APIRouter()
class Room(BaseModel):
    title:str
    description: str
    bedrooms: int
    bathrooms: int
    showers: int
    price: float
ROOMS_FILE ="rooms.json"
def load_rooms():
    if not os.path.exists(ROOMS_FILE):
        return []
    with open (ROOMS_FILE,"r") as file:
        return json.load(file)
    

        
def save_rooms(rooms):
    with open(ROOMS_FILE,"w") as f:
        json.dump(rooms,f,indent=2)
@router.get("/")
def home():
    return {"messege":"Room booking API home "}
@router.post("/rooms")
def create_room(room:Room):
    rooms = load_rooms()
    new_room = {
        "id":str(uuid4()),
        **room.model_dump(),
        "available": True
    }
    rooms.append(new_room)
    save_rooms(rooms)
    return{
        "message":"Room created successfully",
        "room":new_room
    }
@router.get("/rooms")
def get_rooms():
    rooms= load_rooms()
    return rooms
