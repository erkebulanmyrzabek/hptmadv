from django.db import models
from django.core.exceptions import ValidationError
from apps.users.models import Participant
from apps.events.models import Hackathon
import random
import string
from django.core.validators import MinValueValidator, MaxValueValidator

def generate_join_code():
    """Генерация уникального кода из 8 символов (A-Z, 0-9)."""
    characters = string.ascii_uppercase + string.digits
    while True:
        code = ''.join(random.choice(characters) for _ in range(8))
        if not Team.objects.filter(join_code=code).exists():
            return code

class Team(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('active', 'Активна'),
        ('completed', 'Завершена'),
    ]

    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name='teams', help_text="Хакатон, к которому относится команда")
    name = models.CharField(max_length=255, unique=True, help_text="Название команды")
    join_code = models.CharField(max_length=8, unique=True, default=generate_join_code, help_text="Уникальный код для присоединения")
    members = models.ManyToManyField(Participant, related_name='teams', blank=True, help_text="Участники команды")
    created_by = models.ForeignKey(Participant, on_delete=models.SET_NULL, null=True, related_name='created_teams', help_text="Создатель команды")
    max_members = models.PositiveIntegerField(default=4, validators=[MinValueValidator(1), MaxValueValidator(4)], help_text="Максимальное количество участников")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', help_text="Статус команды")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Дата создания команды")

    def clean(self):
        """Валидация количества участников."""
        if self.members.count() > self.max_members:
            raise ValidationError("Количество участников превышает максимальный лимит.")

    def is_full(self):
        """Проверка, заполнена ли команда."""
        return self.members.count() >= self.max_members

    def __str__(self):
        return f"{self.name} (Хакатон: {self.hackathon.title}, Статус: {self.status})"
    


from django.db import models
from .models import Team

class Submission(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE, related_name='submission', help_text="Команда, отправившая решение")
    repo_link = models.URLField(help_text="Ссылка на репозиторий")
    presentation_link = models.URLField(null=True, blank=True, help_text="Ссылка на презентацию (опционально)")
    submitted_at = models.DateTimeField(auto_now_add=True, help_text="Дата отправки решения")

    def __str__(self):
        return f"Решение от {self.team.name} (Хакатон: {self.team.hackathon.title})"