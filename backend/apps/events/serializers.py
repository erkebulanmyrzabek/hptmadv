from rest_framework import serializers
from .models import Hackathon, Tag, Organization, HackathonPrizePlace
from apps.users.models import Participant

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ['id', 'name', 'logo', 'description', 'website', 'telegram', 'instagram']

class HackathonPrizePlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HackathonPrizePlace
        fields = ['place', 'number_of_winners', 'prize_amount', 'xp_reward']

class HackathonSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    participants_count = serializers.IntegerField(source='participants.count', read_only=True)
    total_prize_places = serializers.IntegerField(read_only=True)
    total_prize_amount = serializers.IntegerField(read_only=True)
    hackathon_prizes = HackathonPrizePlaceSerializer(many=True, read_only=True)
    is_participant = serializers.SerializerMethodField()

    class Meta:
        model = Hackathon
        fields = [
            'id', 'title', 'short_description', 'full_description', 'preview_image', 'banner_image',
            'status', 'registration_start_date', 'registration_end_date', 'start_date', 'end_date',
            'type', 'location', 'address', 'faq', 'rules', 'organization', 'tags', 'participants_count',
            'max_participants', 'total_prize_places', 'total_prize_amount', 'hackathon_prizes',
            'created_at', 'is_participant'
        ]

    def get_is_participant(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.participants.filter(id=request.user.id).exists()
        return False