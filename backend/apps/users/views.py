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

# Проверка подписи Telegram (временно закомментирована для теста)
def verify_telegram_data(data):
    received_hash = data.pop('hash', None)
    data_check_string = '\n'.join([f'{k}={v}' for k, v in sorted(data.items())])
    secret_key = hashlib.sha256(settings.JWT_SECRET.encode()).digest()
    calculated_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    return calculated_hash == received_hash

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Participant

class TelegramAuthView(APIView):
    def post(self, request):
        # if not verify_telegram_data(data.copy()):  # Закомментируем проверку для теста
        #     return Response({'error': 'Invalid Telegram data'}, status=status.HTTP_400_BAD_REQUEST)
        #TODO: Еркебулан надо включить проверку для теста
        init_data = request.data
        telegram_id = init_data.get('id')
        
        if not telegram_id:
            return Response({'error': 'Telegram ID не предоставлен'}, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем, существует ли пользователь с таким telegram_id
        try:
            user = Participant.objects.get(telegram_id=telegram_id)
        except Participant.DoesNotExist:
            # Создаем нового пользователя
            user = Participant.objects.create(
                telegram_id=telegram_id,
                username=f"user_{telegram_id}",  # Генерируем временный username
            )
        
        # Генерируем JWT-токены
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