from rest_framework import serializers
from .models import TelegramUser

class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ['telegram_id', 'username', 'first_name', 'last_name', 'photo_url', 'crystals', 'level', 'created_at', 'updated_at']
        read_only_fields = ['crystals', 'level', 'created_at', 'updated_at']