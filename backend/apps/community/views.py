from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Team, Submission
from .serializers import TeamSerializer, SubmissionSerializer
from django.core.exceptions import ValidationError

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(members=self.request.user)

    def create(self, request, *args, **kwargs):
        """Создание новой команды для хакатона."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        hackathon_id = request.data.get('hackathon')
        if Team.objects.filter(hackathon_id=hackathon_id, name=request.data.get('name')).exists():
            raise ValidationError("Команда с таким названием уже существует для этого хакатона.")
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def join(self, request):
        """Присоединение к команде по join_code."""
        join_code = request.data.get('join_code')
        try:
            team = Team.objects.get(join_code=join_code)
            if self.request.user in team.members.all():
                return Response({"detail": "Вы уже в этой команде"}, status=status.HTTP_400_BAD_REQUEST)
            if team.is_full():
                return Response({"detail": "Команда заполнена"}, status=status.HTTP_400_BAD_REQUEST)
            team.members.add(self.request.user)
            serializer = self.get_serializer(team)
            return Response(serializer.data, status=status.HTTP200_OK)
        except Team.DoesNotExist:
            return Response({"detail": "Неверный код приглашения"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def kick(self, request, pk=None):
        """Удаление участника из команды (только для лидера)."""
        team = self.get_object()
        if team.created_by != request.user:
            return Response({"detail": "Только лидер может удалять участников"}, status=status.HTTP_403_FORBIDDEN)
        member_id = request.data.get('member_id')
        member = team.members.filter(id=member_id).first()
        if not member or member == request.user:
            return Response({"detail": "Нельзя удалить себя или несуществующего участника"}, status=status.HTTP_400_BAD_REQUEST)
        team.members.remove(member)
        return Response({"detail": "Участник удалён"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def set_max_members(self, request, pk=None):
        """Изменение максимального количества участников (только для лидера)."""
        team = self.get_object()
        if team.created_by != request.user:
            return Response({"detail": "Только лидер может менять лимит"}, status=status.HTTP_403_FORBIDDEN)
        max_members = request.data.get('max_members')
        if not 1 <= max_members <= 4:
            return Response({"detail": "Лимит должен быть от 1 до 4"}, status=status.HTTP_400_BAD_REQUEST)
        team.max_members = max_members
        team.save()
        return Response({"detail": "Лимит обновлён"}, status=status.HTTP_200_OK)

class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(team__members=self.request.user)

    def create(self, request, *args, **kwargs):
        """Отправка решения для команды."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        team_id = request.data.get('team')
        team = Team.objects.get(id=team_id)
        if self.request.user not in team.members.all():
            return Response({"detail": "Вы не являетесь членом этой команды"}, status=status.HTTP_403_FORBIDDEN)
        if team.submission.exists():
            return Response({"detail": "Решение для этой команды уже отправлено"}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)