from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from apps.users.models import Participant
from admin_panel.models import Organization 

class Hackathon(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='hackathons')
    title = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=[
            ('archived', 'Архив'),
            ('anounce', 'Анонс'),
            ('registration', 'Регистрация'),
            ('in_progress', 'В процессе'),
            ('finished', 'Завершен'),
            ('results_announced', 'Результаты объявлены'),  # Новый статус
        ],
        default='archived'
    )
    type = models.CharField(
        max_length=20,
        choices=[('online', 'Онлайн'), ('offline', 'Офлайн'), ('hybrid', 'Гибрид')],
        default='online'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
class HackathonDetails(models.Model):
    hackathon = models.OneToOneField(Hackathon, on_delete=models.CASCADE, related_name='details')
    short_description = models.TextField(null=True, blank=True)
    full_description = models.TextField(null=True, blank=True)
    preview_image = models.URLField(null=True, blank=True)
    banner_image = models.URLField(null=True, blank=True)
    faq = models.TextField(null=True, blank=True)
    rules = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Детали для {self.hackathon.title}"
    
class HackathonSchedule(models.Model):
    hackathon = models.OneToOneField(Hackathon, on_delete=models.CASCADE, related_name='schedule')
    registration_start_date = models.DateTimeField(null=True, blank=True)
    registration_end_date = models.DateTimeField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    def clean(self):
        if self.registration_start_date and self.registration_end_date and self.registration_start_date > self.registration_end_date:
            raise ValidationError("Дата начала регистрации не может быть позже даты окончания.")
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("Дата начала хакатона не может быть позже даты окончания.")

    def __str__(self):
        return f"Расписание для {self.hackathon.title}"
    

class HackathonLocation(models.Model):
    hackathon = models.OneToOneField(Hackathon, on_delete=models.CASCADE, related_name='location')
    location = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Местоположение для {self.hackathon.title}"
    
    
class HackathonPrizePlace(models.Model):
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name='hackathon_prizes')
    place = models.IntegerField(help_text="Номер призового места (1, 2, 3 и т.д.)")
    number_of_winners = models.PositiveIntegerField(
        default=1,
        help_text="Количество победителей на данном месте"
    )
    prize_amount = models.IntegerField(
        null=True, 
        blank=True, 
        help_text="Сумма приза в валюте или баллах"
    )
    xp_reward = models.PositiveIntegerField(
        default=0,
        help_text="Количество XP за это место"
    )
    winners = models.ManyToManyField(
        'users.Participant',
        blank=True,
        related_name='hackathon_prizes_won',
        help_text="Победители этого места"
    )
    winner_teams = models.ManyToManyField(
        'community.Team',
        blank=True,
        related_name='hackathon_prizes_won',
        help_text="Команды-победители этого места"
    )


    class Meta:
        unique_together = ('hackathon', 'place')
        ordering = ['place']

    def __str__(self):
        winners_count = self.winners.count() + self.winner_teams.count()
        return f"{self.place} место (квота: {self.number_of_winners}, занято: {winners_count}) - {self.prize_amount or 0}₸, {self.xp_reward}XP"


class Tag(models.Model):
    name = models.CharField(max_length=255)
    hackathons = models.ManyToManyField(Hackathon, blank=True, related_name='tags')

    def __str__(self):
        return self.name

class HackathonParticipants(models.Model):
    hackathon = models.OneToOneField(Hackathon, on_delete=models.CASCADE, related_name='participants_info')
    max_participants = models.IntegerField(null=True, blank=True)
    
    def current_participants(self):
        return sum(team.members.count() for team in self.hackathon.teams.all())

    def __str__(self):
        return f"Участники для {self.hackathon.title}"


