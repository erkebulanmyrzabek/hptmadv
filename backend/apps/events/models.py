from django.db import models, transaction
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from apps.users.models import Participant



class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Organization(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    logo = models.URLField(null=True, blank=True)
    banner = models.URLField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    telegram = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Hackathon(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='hackathons')
    title = models.CharField(max_length=255)
    short_description = models.TextField(null=True, blank=True)
    full_description = models.TextField(null=True, blank=True)

    preview_image = models.URLField(null=True, blank=True)
    banner_image = models.URLField(null=True, blank=True)

    STATUS_CHOICES = [
        ('archived', 'Архив'),
        ('anounce', 'Анонс'),
        ('registration', 'Регистрация'),
        ('in_progress', 'В процессе'),
        ('finished', 'Завершен'),
    ]
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='anounce')

    registration_start_date = models.DateTimeField(null=True, blank=True)
    registration_end_date = models.DateTimeField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    TYPE_CHOICES = [
        ('online', 'Онлайн'),
        ('offline', 'Офлайн'),
        ('hybrid', 'Гибрид'),
    ]
    type = models.CharField(max_length=255, choices=TYPE_CHOICES, default='online')

    location = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    faq = models.TextField(null=True, blank=True)
    rules = models.TextField(null=True, blank=True)

    tags = models.ManyToManyField(Tag, blank=True)
    participants = models.ManyToManyField('users.Participant', blank=True, related_name='participated_hackathons')
    max_participants = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def clean(self):
        if self.registration_start_date and self.registration_end_date and self.registration_start_date > self.registration_end_date:
            raise ValidationError("Дата начала регистрации не может быть позже даты окончания.")
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("Дата начала хакатона не может быть позже даты окончания.")

    @property
    def total_prize_places(self):
        """Количество призовых мест"""
        return self.hackathon_prizes.count()

    @property
    def total_prize_amount(self):
        """Общая сумма призов"""
        return self.hackathon_prizes.aggregate(models.Sum('prize_amount'))['prize_amount__sum'] or 0

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

    def distribute_rewards(self):
        """Распределяет награды между победителями"""
        from apps.community.models import Team  # Отложенный импорт
        
        # Распределяем XP и призы для индивидуальных участников
        for winner in self.winners.all():
            winner.xp += self.xp_reward
            if self.prize_amount:
                winner.balance += self.prize_amount
            winner.save()

        # Распределяем XP и призы для команд
        for team in self.winner_teams.all():
            if self.prize_amount:
                prize_per_member = self.prize_amount / team.members.count()
                xp_per_member = self.xp_reward
                
                for member in team.members.all():
                    member.xp += xp_per_member
                    member.balance += prize_per_member
                    member.save()

    def clean(self):
        super().clean()
        if self.pk:
            total_winners = self.winners.count() + self.winner_teams.count()
            if total_winners > self.number_of_winners:
                raise ValidationError(
                    f'Общее количество победителей ({total_winners}) не может превышать {self.number_of_winners}'
                )

    class Meta:
        unique_together = ('hackathon', 'place')
        ordering = ['place']

    def __str__(self):
        winners_count = self.winners.count() + self.winner_teams.count()
        return f"{self.place} место (квота: {self.number_of_winners}, занято: {winners_count}) - {self.prize_amount or 0}₸, {self.xp_reward}XP"

    def save(self, *args, **kwargs):
        if not self.xp_reward:
            if self.place == 1:
                self.xp_reward = 300
            elif self.place == 2:
                self.xp_reward = 200
            elif self.place == 3:
                self.xp_reward = 100
            else:
                self.xp_reward = 50
        super().save(*args, **kwargs)