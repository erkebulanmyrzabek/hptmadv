from django.db import models
from django.core.exceptions import ValidationError
from apps.users.models import Participant
from apps.events.models import Hackathon
import random
import string

def generate_join_code():
    """Генерация уникального кода из 8 символов (A-Z, 0-9)."""
    characters = string.ascii_uppercase + string.digits
    while True:
        code = ''.join(random.choice(characters) for _ in range(8))
        if not Team.objects.filter(join_code=code).exists():
            return code

class Team(models.Model):
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name='teams')
    name = models.CharField(max_length=255)
    join_code = models.CharField(max_length=8, unique=True, default=generate_join_code)
    members = models.ManyToManyField(Participant, related_name='teams', blank=True)
    created_by = models.ForeignKey(Participant, on_delete=models.SET_NULL, null=True, related_name='created_teams')
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.members.count() > 4:
            raise ValidationError("Максимум 4 участника в команде.")

    def __str__(self):
        return f"{self.name} ({self.hackathon.title})"
    

