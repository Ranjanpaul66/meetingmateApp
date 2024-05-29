# calendarapp/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from .models import Event
from django.utils.timezone import now

@shared_task
def send_event_reminders():
    today_events = Event.objects.filter(start_time__date=now().date())
    for event in today_events:
        for participant in event.participants.all():
            send_mail(
                'Event Reminder',
                f'Reminder: You have an event "{event.summary}" starting at {event.start_time}.',
                'from@example.com',
                [participant.email],
                fail_silently=False,
            )
