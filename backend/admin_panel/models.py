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

class AdminConfig(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.key}: {self.value}"
    
class AdminAction(models.Model):
    ACTION_TYPES = [
        ('create_hackathon', 'Create Hackathon'),
        ('edit_hackathon', 'Edit Hackathon'),
        ('archive_hackathon', 'Archive Hackathon'),
        ('ban_user', 'Ban User'),
        ('unban_user', 'Unban User'),
        ('change_role', 'Change Role'),
        ('moderate_news', 'Moderate News'),
        ('register_hackathon', 'Register on Hackathon'),  # Новый тип
    ]

    user = models.ForeignKey('users.Participant', on_delete=models.CASCADE, related_name='admin_actions')
    action_type = models.CharField(max_length=50, choices=ACTION_TYPES)
    target_id = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.telegram_id} - {self.action_type} at {self.timestamp}"