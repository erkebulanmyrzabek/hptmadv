from django.db import models
import random
import string
from django.utils import timezone

# Модель Хакатона
class Hackathon(models.Model):
    STATUS_CHOICES = (
        ('registration', 'Регистрация'),
        ('active', 'Активен'),
        ('completed', 'Завершён'),
    )

    id = models.CharField(max_length=50, primary_key=True, unique=True)  # Уникальный строковый ID
    title = models.CharField(max_length=255)  # Название хакатона
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='registration')
    description = models.TextField()  # Описание
    cover_image = models.URLField(max_length=500, blank=True, null=True)  # URL обложки
    start_date = models.DateTimeField()  # Дата начала
    end_date = models.DateTimeField()  # Дата окончания
    registration_start = models.DateTimeField()  # Начало регистрации
    location = models.CharField(max_length=255)  # Место проведения
    prize_pool = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)  # Призовой фонд
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания
    updated_at = models.DateTimeField(auto_now=True)  # Дата обновления

    def __str__(self):
        return self.title

    def is_registration_open(self):
        """Проверка, открыта ли регистрация."""
        now = timezone.now()
        return self.registration_start <= now < self.start_date and self.status == 'registration'


# Модель Организатора
class HackathonOrganizer(models.Model):
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name='organizers')
    name = models.CharField(max_length=255)  # Название компании
    logo = models.URLField(max_length=500, blank=True, null=True)  # URL логотипа

    def __str__(self):
        return self.name


# Модель Судьи
class HackathonJudge(models.Model):
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name='judges')
    name = models.CharField(max_length=255)  # Имя судьи
    position = models.CharField(max_length=255)  # Должность
    avatar = models.URLField(max_length=500, blank=True, null=True)  # URL аватара

    def __str__(self):
        return f"{self.name} ({self.position})"


# Модель События в расписании
class HackathonScheduleEvent(models.Model):
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name='schedule')
    time = models.DateTimeField()  # Время события
    title = models.CharField(max_length=255)  # Название события
    description = models.TextField()  # Описание события

    def __str__(self):
        return f"{self.title} at {self.time}"


# Модель Правил Хакатона (переименована из Rule)
class HackathonRules(models.Model):
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name='rules')
    text = models.TextField()  # Текст правила

    def __str__(self):
        return self.text


# Модель Участника
class Participant(models.Model):
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name='participants')
    name = models.CharField(max_length=255)  # Имя участника
    role = models.CharField(max_length=100)  # Роль (например, разработчик)
    stack = models.JSONField(default=list)  # Технологический стек (список строк)
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
    name = models.CharField(max_length=255, unique=True)  # Название команды
    stack = models.JSONField(default=list)  # Технологический стек команды
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    max_members = models.PositiveIntegerField(default=5)  # Максимальное количество участников
    invite_code = models.CharField(max_length=10, unique=True, blank=True)  # Код для приглашения

    def save(self, *args, **kwargs):
        """Генерация уникального invite_code при создании команды."""
        if not self.invite_code:
            self.invite_code = self.generate_invite_code()
        super().save(*args, **kwargs)

    def generate_invite_code(self):
        """Генерация уникального кода команды."""
        while True:
            code = 'TEAM' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if not Team.objects.filter(invite_code=code).exists():
                return code

    def is_full(self):
        """Проверка, заполнена ли команда."""
        return self.members.count() >= self.max_members

    def __str__(self):
        return self.name


# Модель Трека
class Track(models.Model):
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name='tracks')
    title = models.CharField(max_length=255)  # Название трека
    description = models.TextField()  # Описание трека
    teams = models.ManyToManyField(Team, related_name='tracks', blank=True)  # Связь с командами

    def participants_count(self):
        """Подсчёт количества участников в треке."""
        return Participant.objects.filter(team__tracks=self).count()

    def teams_count(self):
        """Подсчёт количества команд в треке."""
        return self.teams.count()

    def __str__(self):
        return self.title

