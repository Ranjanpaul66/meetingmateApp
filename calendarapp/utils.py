from google.oauth2 import credentials as google_credentials
from googleapiclient.discovery import build
from django.conf import settings

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from calendarapp.models import Participant, Event


def get_google_calendar_service(token):
    creds = google_credentials.Credentials(token)
    service = build('calendar', 'v3', credentials=creds)
    return service


def fetch_events_from_google_calendar(user):
    social_account = user.socialaccount_set.filter(provider='google').first()
    token = social_account.socialtoken_set.first().token
    service = get_google_calendar_service(token)
    events_result = service.events().list(calendarId='primary').execute()
    events = events_result.get('items', [])
    print(events)
    for event in events:
        event_id = event['id']
        summary = event.get('summary', '')
        description = event.get('description', '')
        start_time = event['start'].get('dateTime')
        end_time = event['end'].get('dateTime')

        # Save event and participants in the database
        # Ensure to check if the event already exists to avoid duplicates
        event_obj, created = Event.objects.get_or_create(
            user=user,
            event_id=event_id,
            defaults={
                'summary': summary,
                'description': description,
                'start_time': start_time,
                'end_time': end_time
            }
        )

        # If the event is created, add participants
        if created:
            attendees = event.get('attendees', [])
            for attendee in attendees:
                Participant.objects.create(
                    event=event_obj,
                    name=attendee.get('displayName', ''),
                    email=attendee.get('email', '')
                )

def send_reminder_email(event):
    participants = event.participants.all()
    for participant in participants:
        subject = f'Reminder: {event.summary}'
        html_message = render_to_string('email_template.html', {'event': event, 'participant': participant})
        plain_message = strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER
        to = participant.email

        send_mail(subject, plain_message, from_email, [to], html_message=html_message)


