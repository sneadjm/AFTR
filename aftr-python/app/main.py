from dotenv import load_dotenv
import os
load_dotenv()

from fastapi import FastAPI
from app.routers import users, friends, photos
from app.database import engine
import app.models as models
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

FRONTEND_URL = os.getenv('FRONTEND_URL')

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

@app.get("/")
def read_root():
    return {"message": "Not everything is broken yet!"}

app.include_router(users.router)
app.include_router(friends.router)
app.include_router(photos.router)

# Allows us to serve image files locally
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

