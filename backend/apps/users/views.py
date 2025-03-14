from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Participant  # Предполагаем, что модель называется Participant
from .serializers.userSerializer import ParticipantSerializer  # Сериализатор (добавим позже)
from django.conf import settings
import hmac
import hashlib

# Проверка подписи Telegram
def verify_telegram_data(data):
    received_hash = data.pop('hash', None)
    data_check_string = '\n'.join([f'{k}={v}' for k, v in sorted(data.items())])
    secret_key = hashlib.sha256(settings.TELEGRAM_BOT_TOKEN.encode()).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    return calculated_hash == received_hash

# TODO: Еркебулан надо добавить валидацию токена
class TelegramAuthView(APIView):
    def post(self, request):
        data = request.data
        if not verify_telegram_data(data.copy()):
            return Response({'error': 'Invalid Telegram data'}, status=status.HTTP_400_BAD_REQUEST)

        telegram_id = data['id']
        user, created = Participant.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={
                'username': data.get('username', f'tg_{telegram_id}'),
                'full_name': f"{data.get('first_name', '')} {data.get('last_name', '')}".strip(),
            }
        )
        # Здесь можно добавить генерацию токена (например, JWT)
        return Response({'message': 'User authenticated', 'user_id': user.id}, status=status.HTTP_200_OK)

class UserViewSet(ReadOnlyModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Возвращаем только текущего пользователя
        return Participant.objects.filter(id=self.request.user.id)