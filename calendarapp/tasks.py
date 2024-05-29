# myapp/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from calendarapp.models import Event

@shared_task
def send_event_reminders():
    now = timezone.now()
    today_end = now.replace(hour=23, minute=59, second=59)

    events_today = Event.objects.filter(start_time__gte=now, start_time__lte=today_end)

    for event in events_today:
        participants = event.participants.all()
        for participant in participants:
            send_mail(
                'Event Reminder',
                f'Hello {participant.name},\n\nThis is a reminder for the event: {event.summary}\n\n'
                f'Start Time: {event.start_time}\nEnd Time: {event.end_time}\n\n'
                f'Description: {event.description}\n\nBest regards,\nYour Event Team',
                'ranjanpaul166.com',  # Replace with your actual sender email
                [participant.email],
                fail_silently=False,
            )
