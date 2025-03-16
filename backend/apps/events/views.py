from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Hackathon, HackathonParticipants
from .serializers import HackathonSerializer
from apps.community.models import Team
from django.utils import timezone


class HackathonViewSet(ReadOnlyModelViewSet):
    queryset = Hackathon.objects.prefetch_related(
        'details', 'schedule', 'location', 'participants_info', 
        'tags', 'hackathon_prizes', 'participants_info__participants'
    )
    serializer_class = HackathonSerializer

    def get_serializer_context(self):
        # Передаем request в контекст сериализатора для проверки is_participant
        return {'request': self.request}

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

