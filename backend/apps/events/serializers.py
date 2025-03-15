from rest_framework import serializers
from .models import (
    Hackathon, HackathonDetails, HackathonSchedule, HackathonLocation, 
    HackathonParticipants, Tag, HackathonPrizePlace
)
from admin_panel.models import Organization
from apps.users.models import Participant
from django.db import models

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'description', 'website', 'telegram', 'instagram']


class HackathonPrizePlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HackathonPrizePlace
        fields = ['place', 'number_of_winners', 'prize_amount', 'xp_reward']


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
    participants_count = serializers.IntegerField(source='participants.count', read_only=True)

    class Meta:
        model = HackathonParticipants
        fields = ['participants_count', 'max_participants']


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

    class Meta:
        model = Hackathon
        fields = [
            'id', 'title', 'status', 'type', 'organization', 'tags', 
            'details', 'schedule', 'location', 'participants_info', 
            'total_prize_places', 'total_prize_amount', 'hackathon_prizes',
            'created_at', 'is_participant'
        ]

    def get_total_prize_amount(self, obj):
        return obj.hackathon_prizes.aggregate(models.Sum('prize_amount'))['prize_amount__sum'] or 0

    def get_is_participant(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.participants_info.participants.filter(id=request.user.id).exists()
        return False