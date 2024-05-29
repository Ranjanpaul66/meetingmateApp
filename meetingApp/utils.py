from calendarapp.models import Participant, Event
import requests


GOOGLE_CALENDAR_EVENTS_URL = 'https://www.googleapis.com/calendar/v3/calendars/primary/events'



def get_calendar_events(access_token):
        response = requests.get(
            GOOGLE_CALENDAR_EVENTS_URL,
            params={'access_token': access_token}
        )
        events = response.json()["items"]
        return events



def save_events(user, events):
    for event in events:
        event_id = event['id']
        summary = event.get('summary', '')
        description = event.get('description', '')
        start_time = event['start'].get('dateTime') or event['start'].get('date')
        end_time = event['end'].get('dateTime') or event['end'].get('date')

        # Check if the event already exists
        if not Event.objects.filter(event_id=event_id).exists():
            # Create the event
            new_event = Event.objects.create(
                user=user,
                event_id=event_id,
                summary=summary,
                description=description,
                start_time=start_time,
                end_time=end_time
            )

            # Add participants
            for attendee in event.get('attendees', []):
                Participant.objects.create(
                    event=new_event,
                    name=attendee.get('email', '').split("@")[0],
                    email=attendee.get('email', '')
                )