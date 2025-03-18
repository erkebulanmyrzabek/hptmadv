from rest_framework import serializers
from .models import (
    Hackathon, HackathonDetails, HackathonSchedule, HackathonLocation, 
    HackathonParticipants, Tag, HackathonPrizePlace, HackathonPrizePlace
)
from admin_panel.models import Organization
from apps.users.models import Participant
from django.db import models
from backend.apps.community.serializers import TeamSerializer
from apps.users.serializers import ParticipantSerializer

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'description', 'website', 'telegram', 'instagram']


class HackathonPrizeSerializer(serializers.ModelSerializer):
    winners = serializers.SerializerMethodField()
    winner_teams = TeamSerializer(many=True, read_only=True)

    class Meta:
        model = HackathonPrizePlace
        fields = ['place', 'number_of_winners', 'prize_amount', 'xp_reward', 'winners', 'winner_teams']

    def get_winners(self, obj):
        # Возвращаем только тех участников, которые привязаны к призовому месту
        winners = obj.winners.all()  # Предполагается, что winners — это ManyToMany поле
        return ParticipantSerializer(winners, many=True).data

class HackathonDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HackathonDetails
        fields = ['short_description', 'full_description', 'preview_image', 'banner_image', 'faq', 'rules']


class HackathonScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = HackathonSchedule
        fields = ['registration_start_date', 'registration_end_date', 'start_date', 'end_date']


class HackathonLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HackathonLocation
        fields = ['location', 'address']


class HackathonParticipantsSerializer(serializers.ModelSerializer):
    current_participants = serializers.SerializerMethodField()

    class Meta:
        model = HackathonParticipants
        fields = ['current_participants', 'max_participants']

    def get_current_participants(self, obj):
        return obj.current_participants()

class HackathonSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    details = HackathonDetailsSerializer(read_only=True)
    schedule = HackathonScheduleSerializer(read_only=True)
    location = HackathonLocationSerializer(read_only=True)
    participants_info = HackathonParticipantsSerializer(read_only=True)
    total_prize_places = serializers.IntegerField(source='hackathon_prizes.count', read_only=True)
    total_prize_amount = serializers.SerializerMethodField()
    hackathon_prizes = HackathonPrizePlaceSerializer(many=True, read_only=True)
    is_participant = serializers.SerializerMethodField()
    teams = TeamSerializer(many=True, read_only=True)

    class Meta:
        model = Hackathon
        fields = [
            'id', 'title', 'status', 'type', 'organization', 'tags', 
            'details', 'schedule', 'location', 'participants_info', 
            'total_prize_places', 'total_prize_amount', 'hackathon_prizes',
            'created_at', 'is_participant', 'teams'
        ]

    def get_total_prize_amount(self, obj):
        return obj.hackathon_prizes.aggregate(models.Sum('prize_amount'))['prize_amount__sum'] or 0

    def get_is_participant(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return any(team.members.filter(id=request.user.id).exists() for team in obj.teams.all())
        return False