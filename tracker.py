import os
from supabase import create_client
from pydantic import BaseModel
from fastapi import FastAPI
from models import Location
from config import supabase

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

class Location(BaseModel):
    user_id: str
    lat: float
    lng: float


app = FastAPI()

# ----------------------------------------------------
# 1. Receive user GPS (device → backend)
# ----------------------------------------------------
@app.post("/update-location")
def update_location(loc: Location):
    supabase.table("locations").upsert({
        "user_id": loc.user_id,
        "lat": loc.lat,
        "lng": loc.lng
    }).execute()

    return {"status": "ok"}


# ----------------------------------------------------
# 2. Return all users' latest coordinates
# ----------------------------------------------------
@app.get("/all-locations")
def all_locations():
    response = supabase.table("locations").select("*").execute()
    return response.data


# ----------------------------------------------------
# 3. Clear tracking table when marathon ends (optional)
# ----------------------------------------------------
@app.post("/clear-locations")
def clear_locations():
    supabase.table("locations").delete().neq("user_id", "").execute()
    return {"status": "cleared"}
