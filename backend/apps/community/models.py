from django.db import models
from apps.users.models import Participant
from apps.events.models import Hackathon


class Team(models.Model):
    name = models.CharField(max_length=100)
    hackathon = models.ForeignKey(Hackathon, related_name='teams', on_delete=models.CASCADE)
    leader = models.ForeignKey(Participant, related_name='led_teams', on_delete=models.CASCADE)
    members = models.ManyToManyField(Participant, related_name='teams')
    max_members = models.PositiveIntegerField(default=4)
    join_code = models.CharField(max_length=8, unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.join_code:
            import uuid
            self.join_code = uuid.uuid4().hex[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.hackathon.name}"