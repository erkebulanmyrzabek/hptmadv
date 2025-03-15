from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class AdminUser(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)  # Храним захэшированный пароль
    name = models.CharField(max_length=100)

    def set_password(self, raw_password):
        """Устанавливает захэшированный пароль."""
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        """Проверяет пароль."""
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.name} ({self.username})"
    

class Organization(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    telegram = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    #TODO потом добавить webinars casecups

    login = models.CharField(max_length=255, blank=True, null=True, unique=True)
    password = models.CharField(max_length=255, blank=True, null=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.name
    
