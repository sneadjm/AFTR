# start up things:
'''
redis-server
celery -A celery_worker.celery_app worker --loglevel=info
pip install celery[redis]
celery -A celery_worker.celery_app worker --beat --loglevel=info
'''

from app.tasks import check_birthdays

check_birthdays.delay()