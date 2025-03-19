from rest_framework import serializers
from .models import Hackathon, HackathonOrganizer, HackathonJudge, HackathonScheduleEvent, HackathonRules, Participant, Team, Track
from apps.users.serializers import TelegramUserSerializer

# Сериализатор для Организаторов
class OrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = HackathonOrganizer
        fields = ['id', 'name', 'logo']

# Сериализатор для Судей
class JudgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HackathonJudge
        fields = ['id', 'name', 'position', 'avatar']

# Сериализатор для Событий расписания
class ScheduleEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = HackathonScheduleEvent
        fields = ['id', 'time', 'title', 'description']

# Сериализатор для Правил
class HackathonRulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HackathonRules
        fields = ['id', 'text']

# Сериализатор для Участников
class ParticipantSerializer(serializers.ModelSerializer):
    user = TelegramUserSerializer(read_only=True)

    class Meta:
        model = Participant
        fields = ['id', 'user', 'name', 'role', 'stack', 'team']

# Сериализатор для Команд
class TeamSerializer(serializers.ModelSerializer):
    members = ParticipantSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'stack', 'status', 'max_members', 'invite_code', 'members']
        read_only_fields = ['invite_code']

    def validate_name(self, value):
        if Team.objects.filter(name=value).exists():
            raise serializers.ValidationError("Команда с таким именем уже существует.")
        return value

# Сериализатор для Треков
class TrackSerializer(serializers.ModelSerializer):
    teams = TeamSerializer(many=True, read_only=True)
    participants_count = serializers.SerializerMethodField()
    teams_count = serializers.SerializerMethodField()

    class Meta:
        model = Track
        fields = ['id', 'title', 'description', 'teams', 'participants_count', 'teams_count']

    def get_participants_count(self, obj):
        return obj.participants_count()

    def get_teams_count(self, obj):
        return obj.teams_count()

# Сериализатор для Хакатона
class HackathonSerializer(serializers.ModelSerializer):
    organizers = OrganizerSerializer(many=True, read_only=True)
    judges = JudgeSerializer(many=True, read_only=True)
    schedule = ScheduleEventSerializer(many=True, read_only=True)
    rules = HackathonRulesSerializer(many=True, read_only=True)
    participants = ParticipantSerializer(many=True, read_only=True)
    teams = TeamSerializer(many=True, read_only=True)
    tracks = TrackSerializer(many=True, read_only=True)

    class Meta:
        model = Hackathon
        fields = [
            'id', 'title', 'status', 'description', 'cover_image', 'start_date', 'end_date',
            'registration_start', 'location', 'prize_pool', 'organizers', 'judges', 'schedule',
            'rules', 'participants', 'teams', 'tracks'
        ]