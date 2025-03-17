import logging
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Participant
from .serializers import ParticipantSerializer
from django.conf import settings
import hmac
import hashlib
from .serializers import ParticipantUpdateSerializer

logger = logging.getLogger(__name__)

# Проверка подписи Telegram (временно закомментирована для теста)
def verify_telegram_data(data):
    if not settings.TELEGRAM_SIGNATURE_VERIFICATION:
        return True

    received_hash = data.get('hash')
    if not received_hash:
        logger.error("Отсутствует hash в данных Telegram: %s", data)
        return False

    # Удаляем hash из данных для проверки
    data_copy = data.copy()
    data_copy.pop('hash', None)

    # Формируем строку для проверки
    data_check_string = '\n'.join([f'{k}={v}' for k, v in sorted(data_copy.items())])
    secret_key = hmac.new("WebAppData".encode(), settings.TELEGRAM_BOT_TOKEN.encode(), hashlib.sha256).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    if calculated_hash != received_hash:
        logger.error("Подпись не совпадает. Рассчитанный hash: %s, Полученный hash: %s", calculated_hash, received_hash)
        return False
    return True

class TelegramAuthView(APIView):
    def post(self, request):
        init_data = request.data.copy()
        print(init_data)  # Копируем данные для проверки

        # Проверяем подпись Telegram
        if not verify_telegram_data(init_data):
            return Response(
                {'error': 'Invalid Telegram data'},
                status=status.HTTP_400_BAD_REQUEST
            )

        telegram_id = init_data.get('id')
        if not telegram_id:
            return Response(
                {'error': 'Telegram ID не предоставлен'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Проверяем, существует ли пользователь с таким telegram_id
        try:
            user = Participant.objects.get(telegram_id=telegram_id)
        except Participant.DoesNotExist:
            # Создаем нового пользователя
            user = Participant.objects.create(
                telegram_id=telegram_id,
                first_name=init_data.get('first_name'),
                last_name=init_data.get('last_name'),
                username=init_data.get('username'),
                #avatar=init_data.get('photo_url'), #TODO: добавить аватарку
            )
        
        # Генерируем JWT-токены``
        refresh = RefreshToken.for_user(user)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_200_OK)

class UserViewSet(ReadOnlyModelViewSet):
    serializer_class = ParticipantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Participant.objects.filter(id=self.request.user.id)

class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = ParticipantUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            updated_user = serializer.save()
            print("Обновленные данные:", updated_user.__dict__)  # Отладка
            return Response({'detail': 'Профиль успешно обновлен'}, status=status.HTTP_200_OK)
        print("Ошибки сериализатора:", serializer.errors)  # Отладка
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)