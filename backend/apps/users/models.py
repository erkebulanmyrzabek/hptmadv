from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class TelegramUserManager(BaseUserManager):
    def create_user(self, telegram_id, username, first_name, last_name=None, photo_url=None, **extra_fields):
        if not telegram_id:
            raise ValueError('Telegram ID обязателен.')
        
        user = self.model(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            photo_url=photo_url,
            **extra_fields
        )
        user.set_unusable_password()  # Пароль не используется, так как авторизация через Telegram
        user.save(using=self._db)
        return user

    def create_superuser(self, telegram_id, username, first_name, last_name=None, photo_url=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(telegram_id, username, first_name, last_name, photo_url, **extra_fields)

class TelegramUser(AbstractBaseUser, PermissionsMixin):
    telegram_id = models.BigIntegerField(unique=True, primary_key=True)  # Telegram ID как первичный ключ
    username = models.CharField(max_length=150, unique=True)  # Telegram username
    first_name = models.CharField(max_length=150)  # Имя
    last_name = models.CharField(max_length=150, blank=True, null=True)  # Фамилия
    photo_url = models.URLField(max_length=500, blank=True, null=True)  # URL фото профиля
    crystals = models.PositiveBigIntegerField(default=0)  # Виртуальные кристаллы
    level = models.PositiveIntegerField(default=1)  # Уровень пользователя
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TelegramUserManager()

    USERNAME_FIELD = 'telegram_id'
    REQUIRED_FIELDS = ['username', 'first_name']

    def __str__(self):
        return f"{self.first_name} ({self.username})"

    @property
    def is_authenticated(self):
        return True