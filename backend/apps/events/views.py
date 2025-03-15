from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Hackathon
from .serializers import HackathonSerializer
from apps.community.models import Team
from django.utils import timezone

class HackathonViewSet(ReadOnlyModelViewSet):
    queryset = Hackathon.objects.all()
    serializer_class = HackathonSerializer

    def get_serializer_context(self):
        # Передаем request в контекст сериализатора для проверки is_participant
        return {'request': self.request}

    def list(self, request, *args, **kwargs):
        # Переопределяем list, если нужно добавить фильтрацию
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def register(self, request, pk=None):
        """Регистрация на хакатон как индивидуальный участник"""
        hackathon = self.get_object()

        # Проверка статуса хакатона
        if hackathon.status != 'registration':
            return Response(
                {'detail': 'Регистрация на этот хакатон сейчас недоступна'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Проверка времени регистрации
        now = timezone.now()
        if hackathon.registration_start_date and now < hackathon.registration_start_date:
            return Response(
                {'detail': 'Регистрация ещё не началась'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if hackathon.registration_end_date and now > hackathon.registration_end_date:
            return Response(
                {'detail': 'Регистрация уже завершена'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Проверка максимального числа участников
        if hackathon.max_participants and hackathon.participants.count() >= hackathon.max_participants:
            return Response(
                {'detail': 'Достигнуто максимальное число участников'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Проверка, зарегистрирован ли пользователь
        user = request.user
        if hackathon.participants.filter(id=user.id).exists():
            return Response(
                {'detail': 'Вы уже зарегистрированы на этот хакатон'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Регистрация пользователя
        hackathon.participants.add(user)
        return Response({'detail': 'Вы успешно зарегистрированы на хакатон'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def create_team(self, request, pk=None):
        """Создание команды для участия в хакатоне"""
        hackathon = self.get_object()
        user = request.user

        # Проверка статуса хакатона
        if hackathon.status != 'registration':
            return Response(
                {'detail': 'Регистрация на этот хакатон сейчас недоступна'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Проверка, состоит ли пользователь в другой команде
        if Team.objects.filter(hackathon=hackathon, members=user).exists():
            return Response(
                {'detail': 'Вы уже состоите в команде для этого хакатона'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Создание команды
        team_name = request.data.get('team_name')
        if not team_name:
            return Response(
                {'detail': 'Не указано название команды'},
                status=status.HTTP_400_BAD_REQUEST
            )

        team = Team.objects.create(
            name=team_name,
            hackathon=hackathon,
            leader=user
        )
        team.members.add(user)
        hackathon.participants.add(user)  # Добавляем лидера в участники хакатона

        return Response({
            'detail': 'Команда успешно создана',
            'team': {
                'id': team.id,
                'name': team.name,
                'join_code': team.join_code,
            }
        }, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def join_team(self, request, pk=None):
        """Присоединение к команде по коду"""
        hackathon = self.get_object()
        user = request.user
        join_code = request.data.get('join_code')

        # Проверка статуса хакатона
        if hackathon.status != 'registration':
            return Response(
                {'detail': 'Регистрация на этот хакатон сейчас недоступна'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Проверка кода команды
        if not join_code:
            return Response(
                {'detail': 'Не указан код команды'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            team = Team.objects.get(hackathon=hackathon, join_code=join_code)
        except Team.DoesNotExist:
            return Response(
                {'detail': 'Команда с таким кодом не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Проверка, состоит ли пользователь в другой команде
        if Team.objects.filter(hackathon=hackathon, members=user).exists():
            return Response(
                {'detail': 'Вы уже состоите в команде для этого хакатона'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Проверка максимального числа участников в команде
        if team.members.count() >= team.max_members:
            return Response(
                {'detail': 'Команда уже заполнена'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Присоединение к команде
        team.members.add(user)
        hackathon.participants.add(user)  # Добавляем участника в хакатон
        return Response({'detail': 'Вы успешно присоединились к команде'}, status=status.HTTP_200_OK)