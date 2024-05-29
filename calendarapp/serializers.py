from rest_framework import serializers
from .models import Event, Participant

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['name', 'email']

class EventSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True)

    class Meta:
        model = Event
        fields = ['event_id', 'summary', 'description', 'start_time', 'end_time', 'participants']
