from rest_framework import serializers
from .models import Team

class TeamSerializer(serializers.ModelSerializer):
    members_count = serializers.IntegerField(source='members.count', read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'join_code', 'members_count', 'created_at']