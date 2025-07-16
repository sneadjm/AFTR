from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from app import models, schemas, database, auth
from typing import List, Optional
import shutil
import os
from uuid import uuid4
from datetime import date

router = APIRouter(prefix="/friends", tags=["Friends"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=schemas.FriendOut)
def create_friend(
    friend: schemas.FriendCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    new_friend = models.Friend(
        name=friend.name,
        birthday=friend.birthday,
        owner_id=current_user.id
    )
    db.add(new_friend)
    db.commit()
    db.refresh(new_friend)
    return new_friend

@router.post("/{friend_id}/upload-photo", response_model=schemas.FriendOut)
def upload_photo(
    friend_id: int,
    photo: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    friend = db.query(models.Friend).filter_by(id=friend_id, owner_id=current_user.id).first()
    if not friend:
        raise HTTPException(status_code=404, detail="Friend not found")

    file_ext = photo.filename.split(".")[-1]
    file_name = f"{uuid4()}.{file_ext}"
    file_path = os.path.join(UPLOAD_DIR, file_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)

    friend.photo_url = f"/{UPLOAD_DIR}{file_name}"
    db.commit()
    db.refresh(friend)
    return friend

@router.get("/", response_model=List[schemas.FriendOut])
def get_friends(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return db.query(models.Friend).filter_by(owner_id=current_user.id).all()

@router.get("/{friend_id}", response_model=schemas.FriendOut)
def get_friend(
    friend_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    friend = db.query(models.Friend).filter_by(id=friend_id, owner_id=current_user.id).first()
    if not friend:
        raise HTTPException(status_code=404, detail="Friend not found")
    return friend

@router.put("/{friend_id}", response_model=schemas.FriendOut)
def update_friend(
    friend_id: int,
    update_data: schemas.FriendCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    friend = db.query(models.Friend).filter_by(id=friend_id, owner_id=current_user.id).first()
    if not friend:
        raise HTTPException(status_code=404, detail="Friend not found")

    friend.name = update_data.name
    friend.birthday = update_data.birthday
    db.commit()
    db.refresh(friend)
    return friend

@router.delete("/{friend_id}", status_code=204)
def delete_friend(
    friend_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    friend = db.query(models.Friend).filter_by(id=friend_id, owner_id=current_user.id).first()
    if not friend:
        raise HTTPException(status_code=404, detail="Friend not found")

    db.delete(friend)
    db.commit()
    return