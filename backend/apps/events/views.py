import logging
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Hackathon, Team, Participant
from .serializers import HackathonSerializer, TeamSerializer

logger = logging.getLogger(__name__)

class HackathonViewSet(viewsets.ModelViewSet):
    queryset = Hackathon.objects.all()
    serializer_class = HackathonSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        logger.info(f"Запрошен список хакатонов. Количество: {len(queryset)}")
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        logger.info(f"Запрошен хакатон с ID {instance.id}: {instance.title}")
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def create_team(self, request, pk=None):
        hackathon = self.get_object()
        
        if not hackathon.is_registration_open():
            logger.warning(f"Попытка создать команду для хакатона {hackathon.id}, но регистрация закрыта.")
            return Response({'error': 'Регистрация на хакатон закрыта.'}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        participant = Participant.objects.filter(hackathon=hackathon, user=user).first()
        if participant and participant.team:
            logger.warning(f"Пользователь {user.username} уже состоит в команде {participant.team.name}.")
            return Response({'error': 'Вы уже состоите в команде.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TeamSerializer(data={
            'hackathon': hackathon.id,
            'name': request.data.get('name'),
            'stack': request.data.get('stack', ['Unknown']),
            'status': 'open',
            'max_members': 5
        })
        if serializer.is_valid():
            team = serializer.save()
            if not participant:
                participant = Participant.objects.create(
                    hackathon=hackathon,
                    user=user,
                    name=user.first_name,
                    role='Участник',
                    stack=['Unknown']
                )
            participant.team = team
            participant.save()
            logger.info(f"Создана команда {team.name} для хакатона {hackathon.id} пользователем {user.username}.")
            return Response(TeamSerializer(team).data, status=status.HTTP_201_CREATED)
        logger.error(f"Ошибка при создании команды: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def join_team(self, request, pk=None):
        hackathon = self.get_object()
        
        if not hackathon.is_registration_open():
            logger.warning(f"Попытка присоединиться к команде для хакатона {hackathon.id}, но регистрация закрыта.")
            return Response({'error': 'Регистрация на хакатон закрыта.'}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        participant = Participant.objects.filter(hackathon=hackathon, user=user).first()
        if participant and participant.team:
            logger.warning(f"Пользователь {user.username} уже состоит в команде {participant.team.name}.")
            return Response({'error': 'Вы уже состоите в команде.'}, status=status.HTTP_400_BAD_REQUEST)

        team_code = request.data.get('teamCode')
        if not team_code:
            logger.warning(f"Попытка присоединиться к команде без указания кода.")
            return Response({'error': 'Код команды обязателен.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            team = hackathon.teams.get(invite_code=team_code)
            if team.is_full():
                logger.warning(f"Команда {team.name} заполнена, пользователь {user.username} не может присоединиться.")
                return Response({'error': 'Команда заполнена.'}, status=status.HTTP_400_BAD_REQUEST)

            if not participant:
                participant = Participant.objects.create(
                    hackathon=hackathon,
                    user=user,
                    name=user.first_name,
                    role='Участник',
                    stack=['Unknown']
                )
            participant.team = team
            participant.save()
            logger.info(f"Пользователь {user.username} присоединился к команде {team.name} в хакатоне {hackathon.id}.")
            return Response(TeamSerializer(team).data, status=status.HTTP_200_OK)
        except Team.DoesNotExist:
            logger.warning(f"Команда с кодом {team_code} не найдена для хакатона {hackathon.id}.")
            return Response({'error': 'Команда с таким кодом не найдена.'}, status=status.HTTP_404_NOT_FOUND)