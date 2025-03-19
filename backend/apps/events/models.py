from django.db import models
import random
import string
from django.utils import timezone
from apps.users.models import TelegramUser

# Модель Хакатона
class Hackathon(models.Model):
    STATUS_CHOICES = (
        ('registration', 'Регистрация'),
        ('active', 'Активен'),
        ('completed', 'Завершён'),
        ('upcoming', 'Скоро'),
    )

    id = models.CharField(max_length=50, primary_key=True, unique=True)
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='registration')
    description = models.TextField()
    cover_image = models.URLField(max_length=500, blank=True, null=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    registration_start = models.DateTimeField()
    location = models.CharField(max_length=255)
    prize_pool = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def is_registration_open(self):
        now = timezone.now()
        return self.registration_start <= now < self.start_date and self.status == 'registration'

# Модель Организатора
class HackathonOrganizer(models.Model):
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name='organizers')
    name = models.CharField(max_length=255)
    logo = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name

# Модель Судьи
class HackathonJudge(models.Model):
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name='judges')
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    avatar = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.position})"

# Модель События в расписании
class HackathonScheduleEvent(models.Model):
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name='schedule')
    time = models.DateTimeField()
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.title} at {self.time}"

# Модель Правил Хакатона
class HackathonRules(models.Model):
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name='rules')
    text = models.TextField()

    def __str__(self):
        return self.text

# Модель Участника
class Participant(models.Model):
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name='participations')
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=100)
    stack = models.JSONField(default=list)
    team = models.ForeignKey('Team', on_delete=models.SET_NULL, null=True, blank=True, related_name='members')

    def __str__(self):
        return self.name

# Модель Команды
class Team(models.Model):
    STATUS_CHOICES = (
        ('open', 'Открыта'),
        ('closed', 'Закрыта'),
    )

    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name='teams')
    name = models.CharField(max_length=255, unique=True)
    stack = models.JSONField(default=list)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    max_members = models.PositiveIntegerField(default=5)
    invite_code = models.CharField(max_length=10, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = self.generate_invite_code()
        super().save(*args, **kwargs)

    def generate_invite_code(self):
        while True:
            code = 'TEAM' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if not Team.objects.filter(invite_code=code).exists():
                return code

    def is_full(self):
        return self.members.count() >= self.max_members

    def __str__(self):
        return self.name

# Модель Трека
class Track(models.Model):
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name='tracks')
    title = models.CharField(max_length=255)
    description = models.TextField()
    teams = models.ManyToManyField(Team, related_name='tracks', blank=True)

    def participants_count(self):
        return Participant.objects.filter(team__tracks=self).count()

    def teams_count(self):
        return self.teams.count()

    def __str__(self):
        return self.title