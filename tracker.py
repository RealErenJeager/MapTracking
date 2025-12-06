import os
from supabase import create_client
from pydantic import BaseModel
from fastapi import FastAPI

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

class Location(BaseModel):
    user_id: str
    lat: float
    lng: float

app = FastAPI()

@app.post("/update-location")
def update_location(loc: Location):
    supabase.table("locations").upsert({
        "user_id": loc.user_id,
        "lat": loc.lat,
        "lng": loc.lng
    }).execute()

    return {"status": "ok"}

@app.get("/all-locations")
def all_locations():
    response = supabase.table("locations").select("*").execute()
    return response.data

@app.post("/clear-locations")
def clear_locations():
    supabase.table("locations").delete().neq("user_id", "").execute()
    return {"status": "cleared"}
