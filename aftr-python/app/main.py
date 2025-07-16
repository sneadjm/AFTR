from fastapi import FastAPI
from routers import users, friends, photos
from database import engine
import models
from fastapi.staticfiles import StaticFiles

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(friends.router)
app.include_router(photos.router)

# Allows us to serve image files locally
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

