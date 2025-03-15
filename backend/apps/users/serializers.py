from rest_framework import serializers
from .models import Participant

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = [
            'id', 'telegram_id', 'username', 'first_name', 'last_name', 'phone_number', 'email',
            'balance', 'xp', 'level', 'gender', 'birth_date', 'city', 'country', 'address',
            'avatar', 'bio', 'is_verified', 'created_at', 'updated_at', 'language', 'theme'
        ]

class ParticipantUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = [
            'first_name', 'last_name', 'phone_number', 'email', 'gender', 'birth_date',
            'city', 'country', 'address', 'bio'
        ]