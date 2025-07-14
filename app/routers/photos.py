from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app import models, database, auth
from datetime import datetime
import os
import shutil
from uuid import uuid4
from PIL import Image
from PIL.ExifTags import TAGS

router = APIRouter(prefix="/photos", tags=["Photos"])

UPLOAD_DIR = "user_photos/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def extract_taken_date(photo_path: str) -> datetime.date:
    try:
        image = Image.open(photo_path)
        exif_data = image._getexif()
        if not exif_data:
            return None

        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id)
            if tag == 'DateTimeOriginal':
                return datetime.strptime(value, '%Y:%m:%d %H:%M:%S').date()
    except Exception:
        return None

@router.post("/upload", response_model=schemas.PhotoOut)
def upload_photo(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    file_ext = file.filename.split(".")[-1]
    filename = f"{uuid4()}.{file_ext}"
    path = os.path.join(UPLOAD_DIR, filename)

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    taken_at = extract_taken_date(path)

    photo = models.Photo(
        filename=f"/{UPLOAD_DIR}{filename}",
        taken_at=taken_at,
        owner_id=current_user.id
    )
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo

@router.get("/suggest/{friend_id}", response_model=List[schemas.PhotoOut])
def suggest_photos(
    friend_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    friend = db.query(models.Friend).filter_by(id=friend_id, owner_id=current_user.id).first()
    if not friend:
        raise HTTPException(status_code=404, detail="Friend not found")

    birthday = friend.birthday
    yearless_birthday = (birthday.month, birthday.day)

    # Find user photos taken on that month/day (any year)
    suggested = db.query(models.Photo).filter(
        models.Photo.owner_id == current_user.id,
        models.Photo.taken_at.isnot(None)
    ).all()

    # Match month/day
    matching_photos = [
        photo for photo in suggested
        if (photo.taken_at.month, photo.taken_at.day) == yearless_birthday
    ]

    return matching_photos