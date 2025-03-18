from rest_framework import serializers
from apps.users.serializers import ParticipantSerializer
from .models import Team, Submission

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['id', 'team', 'repo_link', 'presentation_link', 'submitted_at']
        read_only_fields = ['submitted_at']

class TeamSerializer(serializers.ModelSerializer):
    members = ParticipantSerializer(many=True, read_only=True)
    submission = SubmissionSerializer(read_only=True)
    is_full = serializers.BooleanField(read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'hackathon', 'name', 'join_code', 'members', 'created_by', 'max_members', 'status', 'is_full', 'submission', 'created_at']
        read_only_fields = ['join_code', 'created_at', 'is_full', 'submission']

    def create(self, validated_data):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError("Аутентификация обязательна.")
        validated_data['created_by'] = request.user
        validated_data['members'] = [request.user]
        return super().create(validated_data)

    def validate_name(self, value):
        hackathon_id = self.initial_data.get('hackathon')
        if Team.objects.filter(hackathon_id=hackathon_id, name=value).exists():
            raise serializers.ValidationError("Команда с таким названием уже существует для этого хакатона.")
        return value