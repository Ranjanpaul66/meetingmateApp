# myapp/periodic_tasks.py
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json

def create_periodic_task():
    schedule, created = CrontabSchedule.objects.get_or_create(
        hour=8, minute=0  # Adjust the time as needed
    )

    PeriodicTask.objects.get_or_create(
        crontab=schedule,
        name='Send Event Reminders',
        task='myapp.tasks.send_event_reminders',
        defaults={'kwargs': json.dumps({})},
    )
