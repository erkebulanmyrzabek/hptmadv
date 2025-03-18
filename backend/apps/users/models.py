from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import MinValueValidator, MaxValueValidator

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
        ('Almaty', 'Алматы'), ('Nur-Sultan', 'Нур-Султан'), ('Shymkent', 'Шымкент'),
        ('Taraz', 'Тараз'), ('Aktobe', 'Актобе'), ('Kyzylorda', 'Кызылорда'),
        ('Kostanay', 'Костанай'), ('Pavlodar', 'Павлодар'), ('Oral', 'Орал'),
        ('Atyrau', 'Атырау'), ('Zhambyl', 'Жамбыл'), ('Karagandy', 'Караганда'),
        ('Kokshetau', 'Кокшетау'), ('Mangystau', 'Мангистау'), ('Petropavl', 'Петропавловск'),
        ('Taldykorgan', 'Талдыкорган'), ('Turkistan', 'Туркестан'), ('Ust-Kamenogorsk', 'Усть-Каменогорск'),
    ]

    telegram_id = models.CharField(max_length=255, unique=True, help_text="Уникальный ID Telegram пользователя")
    first_name = models.CharField(max_length=64, null=True, blank=True, help_text="Имя пользователя")
    last_name = models.CharField(max_length=64, null=True, blank=True, help_text="Фамилия пользователя")
    is_banned = models.BooleanField(default=False, help_text="Блокировка пользователя")
    phone_number = models.CharField(max_length=11, unique=True, null=True, blank=True, help_text="Номер телефона")
    email = models.EmailField(unique=True, null=True, blank=True, help_text="Электронная почта")
    balance = models.IntegerField(default=0, help_text="Баланс пользователя")
    xp = models.IntegerField(default=0, help_text="Опытные очки (XP)")
    level = models.IntegerField(default=1, help_text="Уровень пользователя")
    is_premium = models.BooleanField(default=False, help_text="Премиум-статус")
    skills_list = models.ManyToManyField(Skill, blank=True, related_name="users_with_skill", help_text="Список навыков")
    certificates = models.ManyToManyField(Certificate, blank=True, related_name="certificate_holders", help_text="Сертификаты")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True, help_text="Пол")
    birth_date = models.DateField(null=True, blank=True, help_text="Дата рождения")
    city = models.CharField(max_length=255, choices=CITY_CHOICES, null=True, blank=True, help_text="Город")
    country = models.CharField(max_length=255, null=True, blank=True, help_text="Страна")
    address = models.CharField(max_length=255, null=True, blank=True, help_text="Адрес")
    avatar = models.URLField(null=True, blank=True, help_text="Ссылка на аватар")
    bio = models.CharField(max_length=60, null=True, blank=True, help_text="Краткая биография")
    is_verified = models.BooleanField(default=False, help_text="Подтверждён ли аккаунт")
    achievements = models.ManyToManyField(Achievement, blank=True, related_name="achieved_by", help_text="Достижения")
    hackathons = models.ManyToManyField('events.Hackathon', blank=True, related_name='participants', help_text="Хакатоны, в которых участвовал")
    friends = models.ManyToManyField('self', blank=True, symmetrical=True, related_name='friend_of', help_text="Список друзей")
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, null=True, blank=True, help_text="Тема интерфейса")
    language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, null=True, blank=True, default='ru', help_text="Язык интерфейса")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Дата создания аккаунта")
    updated_at = models.DateTimeField(auto_now=True, help_text="Дата последнего обновления")
    password = models.CharField(max_length=128, null=True, blank=True, help_text="Пароль")
    USERNAME_FIELD = 'telegram_id'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def calculate_level(self):
        """Расчёт уровня на основе опыта."""
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
        """XP, необходимый для следующего уровня."""
        return 100 + (self.level - 1) * 50

    def get_current_level_xp(self):
        """XP, необходимый для текущего уровня."""
        return 0 if self.level == 1 else 100 + (self.level - 2) * 50

    def hackathon_count(self):
        """Количество хакатонов, в которых участвовал."""
        return self.hackathons.count()

    def __str__(self):
        return f"{self.first_name or 'Unknown'} {self.last_name or ''} (@{self.telegram_id})"