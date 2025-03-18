from rest_framework import serializers
from apps.events.models import Hackathon
from apps.events.serializers import HackathonSerializer

class OrganizerHackathonSerializer(HackathonSerializer):
    class Meta(HackathonSerializer.Meta):
        fields = HackathonSerializer.Meta.fields + ['teams', 'participants_info']