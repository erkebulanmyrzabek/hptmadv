from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Hackathon
from apps.community.models import Team
from .serializers import HackathonSerializer, TeamSerializer
from django.utils import timezone
from django.shortcuts import get_object_or_404

class HackathonViewSet(ReadOnlyModelViewSet):
    queryset = Hackathon.objects.prefetch_related(
        'details', 'schedule', 'location', 'participants_info', 
        'tags', 'hackathon_prizes', 'teams', 'teams__members'
    )
    serializer_class = HackathonSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def register(self, request, pk=None):
        hackathon = self.get_object()
        user = request.user
        schedule = hackathon.schedule

        # Проверка статуса и дат
        if hackathon.status != 'registration':
            return Response({"detail": "Регистрация на этот хакатон закрыта"}, status=status.HTTP_400_BAD_REQUEST)
        if not (schedule.registration_start_date <= timezone.now() <= schedule.registration_end_date):
            return Response({"detail": "Период регистрации истек"}, status=status.HTTP_400_BAD_REQUEST)

        participants_info = hackathon.participants_info
        if (participants_info.max_participants and 
            participants_info.current_participants() >= participants_info.max_participants):
            return Response({"detail": "Достигнут лимит участников"}, status=status.HTTP_400_BAD_REQUEST)

        # Проверка, участвует ли пользователь уже
        if any(team.members.filter(id=user.id).exists() for team in hackathon.teams.all()):
            return Response({"detail": "Вы уже зарегистрированы"}, status=status.HTTP_400_BAD_REQUEST)

        registration_type = request.data.get('type')
        if registration_type == 'solo':
            team = Team.objects.create(
                hackathon=hackathon,
                name=f"Solo_{user.telegram_id}",
                created_by=user
            )
            team.members.add(user)
            return Response({"detail": "Успешно зарегистрированы как соло-участник"}, status=status.HTTP_200_OK)

        elif registration_type == 'create_team':
            team_name = request.data.get('team_name')
            if not team_name:
                return Response({"detail": "Укажите название команды"}, status=status.HTTP_400_BAD_REQUEST)
            team = Team.objects.create(hackathon=hackathon, name=team_name, created_by=user)
            team.members.add(user)
            return Response({"detail": "Команда создана", "team": TeamSerializer(team).data}, status=status.HTTP_201_CREATED)

        elif registration_type == 'join_team':
            join_code = request.data.get('join_code')
            team = get_object_or_404(Team, join_code=join_code, hackathon=hackathon)
            if team.members.count() >= 4:
                return Response({"detail": "Команда заполнена"}, status=status.HTTP_400_BAD_REQUEST)
            team.members.add(user)
            return Response({"detail": "Успешно присоединены к команде"}, status=status.HTTP_200_OK)

        return Response({"detail": "Неверный тип регистрации"}, status=status.HTTP_400_BAD_REQUEST)