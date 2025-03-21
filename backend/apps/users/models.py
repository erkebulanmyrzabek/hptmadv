from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

# Create your models here.
class Skill(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Certificate(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class Achievement(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name

class CustomUserManager(UserManager):
    def create_superuser(self, telegram_id, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('username', f"user_{telegram_id}")
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(telegram_id, password=password, **extra_fields)

    def create_user(self, telegram_id, password=None, **extra_fields):
        if not telegram_id:
            raise ValueError('The Telegram ID must be set')
        user = self.model(telegram_id=telegram_id, **extra_fields)
        user.set_password(password)
        user.save()
        return user

class Participant(AbstractUser):
    GENDER_CHOICES = [
        ('male', 'Мужской'),
        ('female', 'Женский'),
    ]

    THEME_CHOICES = [
        ('dark', 'Темный'),
        ('light', 'Светлый'),
    ]

    LANGUAGE_CHOICES = [
        ('ru', 'Русский'),
        ('en', 'Английский'),
    ]

    CITY_CHOICES = [
        ('Almaty', 'Алматы'),
        ('Nur-Sultan', 'Нур-Султан'),
        ('Shymkent', 'Шымкент'),
        ('Taraz', 'Тараз'),
        ('Aktobe', 'Актобе'),
        ('Kyzylorda', 'Кызылорда'),
        ('Kostanay', 'Костанай'),
        ('Pavlodar', 'Павлодар'),
        ('Oral', 'Орал'),
        ('Atyrau', 'Атырау'),
        ('Zhambyl', 'Жамбыл'),
        ('Karagandy', 'Караганда'),
        ('Kokshetau', 'Кокшетау'),
        ('Mangystau', 'Мангистау'),
        ('Petropavl', 'Петропавловск'),
        ('Taldykorgan', 'Талдыкорган'),
        ('Turkistan', 'Туркестан'),
        ('Ust-Kamenogorsk', 'Усть-Каменогорск'),
        # TODO дополнить список городов
    ]
    
    telegram_id = models.CharField(max_length=255, unique=True)
    # username уже есть в AbstractUser, оставляем его
    first_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    is_banned = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=11, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    balance = models.IntegerField(default=0)
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    is_premium = models.BooleanField(default=False)
    skills_list = models.ManyToManyField(Skill, blank=True)
    certificates = models.ManyToManyField(Certificate, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=255, choices=CITY_CHOICES, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    avatar = models.URLField(null=True, blank=True)
    bio = models.CharField(null=True, blank=True, max_length=60)
    is_verified = models.BooleanField(default=False)
    achievements = models.ManyToManyField(Achievement, blank=True)
    hackathons = models.ManyToManyField('events.Hackathon', blank=True, related_name='participant_list')
    friends = models.ManyToManyField('self', blank=True)
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, null=True, blank=True)
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, null=True, blank=True)
    password = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Поля для аутентификации
    USERNAME_FIELD = 'telegram_id'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def calculate_level(self):
        xp = self.xp
        level = 1
        required_xp = 0

        while xp >= required_xp:
            level += 1
            required_xp = 100 + (level - 2) * 50

        return level - 1

    def save(self, *args, **kwargs):
        self.level = self.calculate_level()
        super().save(*args, **kwargs)

    def get_next_level_xp(self):
        return 100 + (self.level - 1) * 50

    def get_current_level_xp(self):
        if self.level == 1:
            return 0
        return 100 + (self.level - 2) * 50

    def hackathon_count(self):
        return self.hackathons.count()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.telegram_id}"