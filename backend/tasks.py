from datetime import timedelta, datetime
from django.conf import settings
from django.utils import timezone
from huey import crontab
from huey.contrib.djhuey import db_periodic_task, db_task, periodic_task
from backend.utils.email import send_notification_email
from backend.models import Event, UserRegisterEvent
import os

SEND_BEFORE = [
    (7, '一周后'),
    (3, '三天后'),
    (1, '明天')
]
TEMP_FILE_PATH = os.path.join(settings.FILES_DIR, 'temp/')
TEMP_FILE_EXTS = ['.xls', '.xlsx', '.xlsm']

@db_periodic_task(crontab(minute='0', hour='0'))  # Remember to -8 as it is ISO time
def recent_event_notification():
    span = timedelta(days=1)
    for before_days in SEND_BEFORE:
        before = timedelta(days=before_days[0])
        now = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        event_list = Event.objects.filter(
            start_time__gte=now + before,
            start_time__lt=now + before + span
        )
        for event in event_list:
            ure_list = UserRegisterEvent.objects.filter(event=event)
            for ure in ure_list:
                send_notification_email(ure, before_days[1])


@periodic_task(crontab(minute='0', hour='0'))
def clear_temp_files():
    for file_name in os.listdir(TEMP_FILE_PATH):
        if os.path.splitext(file_name)[1] in TEMP_FILE_EXTS:
            os.remove(file_name)

