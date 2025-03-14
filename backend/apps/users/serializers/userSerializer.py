from rest_framework import serializers
from ..models import Participant

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = ['id', 'telegram_id', 'username', 'full_name', 'xp', 'balance', 
                  'level', 'avatar', 'bio', 'city', 'country', 'address', 
                  'skills_list', 'certificates', 'achievements', 'hackathons', 
                  'friends', 'theme', 'language']