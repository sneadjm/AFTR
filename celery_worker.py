from celery import Celery
import os
from dotenv import load_dotenv
from celery.schedules import crontab

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "aftr_app",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery_app.conf.timezone = "UTC"

celery_app.conf.beat_schedule = {
    "check-birthdays-daily": {
        "task": "aftr_app.tasks.check_birthdays",
        "schedule": crontab(hour=0, minute=0),  # every day at midnight UTC
    }
}