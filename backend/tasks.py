from datetime import timedelta, datetime
from django.conf import settings
from django.utils import timezone
from huey import crontab
from huey.contrib.djhuey import db_periodic_task, db_task
from backend.utils.email import send_notification_email
from backend.models import Event, UserRegisterEvent

SEND_BEFORE = [
    (7, '一周'),
    (3, '三天')
]

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
            href = 'http://%s/event/%s' % (settings.SITE_HOST_NAME, event.id)
            message = '您注册的<a href="%s">event.title</a>将于%s后在%s举行，请按时参加。'
            message %= (href, before_days[1], event.location)
            ure_list = UserRegisterEvent.objects.filter(event=event)
            for ure in ure_list:
                send_notification_email(ure.user, message)
