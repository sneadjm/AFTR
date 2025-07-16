from datetime import datetime, timedelta
from database import SessionLocal
import models
from celery_worker import celery_app
from utils import email

@celery_app.task
def check_birthdays():
    db = SessionLocal()
    try:
        today = datetime.utcnow().date()
        tomorrow = today + timedelta(days=1)

        users = db.query(models.User).all()

        for user in users:
            for friend in user.friends:
                if friend.birthday.month == today.month and friend.birthday.day == today.day:
                    print(f"🎉 TODAY: Notify {user.email} — it's {friend.name}'s birthday!")

                elif friend.birthday.month == tomorrow.month and friend.birthday.day == tomorrow.day:
                    print(f"📅 Reminder for {user.email}: Tomorrow is {friend.name}'s birthday.")
    finally:
        db.close()

@celery_app.task
def check_birthdays():
    db = SessionLocal()
    try:
        today = datetime.utcnow().date()
        tomorrow = today + timedelta(days=1)

        users = db.query(models.User).all()

        for user in users:
            messages = []

            for friend in user.friends:
                bday = friend.birthday
                if (bday.month, bday.day) == (today.month, today.day):
                    messages.append(f"🎉 It's {friend.name}'s birthday today!")

                elif (bday.month, bday.day) == (tomorrow.month, tomorrow.day):
                    messages.append(f"📅 Tomorrow is {friend.name}'s birthday!")

            if messages:
                body = "\n".join(messages)
                email.send_email(
                    to_email=user.email,
                    subject="🎂 Birthday Reminder",
                    body=body
                )
    finally:
        db.close()