from django.shortcuts import render

# Create your views here.
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import TelegramUser
from .serializers import TelegramUserSerializer
from .utils import verify_telegram_init_data

logger = logging.getLogger(__name__)

class TelegramLoginView(APIView):
    def post(self, request):
        init_data = request.data.get('initData')
        if not init_data:
            logger.warning("Попытка авторизации без initData.")
            return Response({'error': 'initData обязателен.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Проверяем initData
            user_data = verify_telegram_init_data(init_data)
            telegram_id = user_data.get('id')
            username = user_data.get('username', f"user_{telegram_id}")
            first_name = user_data.get('first_name', 'Unknown')
            last_name = user_data.get('last_name', '')
            photo_url = user_data.get('photo_url', '')

            # Создаём или обновляем пользователя
            user, created = TelegramUser.objects.get_or_create(
                telegram_id=telegram_id,
                defaults={
                    'username': username,
                    'first_name': first_name,
                    'last_name': last_name,
                    'photo_url': photo_url,
                }
            )
            if not created:
                # Обновляем данные, если пользователь уже существует
                user.username = username
                user.first_name = first_name
                user.last_name = last_name
                user.photo_url = photo_url
                user.save()
                logger.info(f"Обновлены данные пользователя {username} (ID: {telegram_id}).")
            else:
                logger.info(f"Создан новый пользователь {username} (ID: {telegram_id}).")

            # Генерируем JWT-токены
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            # Сериализуем данные пользователя
            user_serializer = TelegramUserSerializer(user)

            return Response({
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': user_serializer.data
            }, status=status.HTTP_200_OK)

        except ValueError as e:
            logger.error(f"Ошибка проверки initData: {str(e)}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Неожиданная ошибка при авторизации: {str(e)}", exc_info=True)
            return Response({'error': 'Произошла ошибка при авторизации.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)