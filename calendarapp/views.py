from rest_framework import generics, permissions
from rest_framework.views import APIView
from .models import Event
from .serializers import EventSerializer
from rest_framework.response import Response
from rest_framework import status

class EventListView(APIView):
    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)






