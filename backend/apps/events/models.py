from django.db import models
from django.utils import timezone
from apps.users.models import Participant  # Предполагаю, что Participant определен в users

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

    events = models.ManyToManyField('Event', blank=True)  # Ссылка на Event

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    EVENT_TYPE_CHOICES = [
        ('hackathon', 'Хакатон'),
        ('webinar', 'Вебинар'),
        ('case_cup', 'Кейс-кап'),
        ('news', 'Новость'),
    ]

    event_type = models.CharField(max_length=255, choices=EVENT_TYPE_CHOICES)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_event_type_display()} ({self.organization})"

class Hackathon(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE, primary_key=True, related_name='hackathon')
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
    participants = models.ManyToManyField(Participant, blank=True)
    max_participants = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.event.event_type != 'hackathon':
            raise ValueError("Hackathon can only be linked to an Event with type 'hackathon'")
        super().save(*args, **kwargs)

    @property
    def total_prize_places(self):
        """Количество призовых мест"""
        return self.prize_places.count()

    @property
    def total_prize_amount(self):
        """Общая сумма призов"""
        return self.prize_places.aggregate(models.Sum('prize_amount'))['prize_amount__sum'] or 0

class HackathonPrizePlace(models.Model):
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name='prize_places')
    place = models.IntegerField(help_text="Номер призового места (1, 2, 3 и т.д.)")
    prize_amount = models.IntegerField(null=True, blank=True, help_text="Сумма приза в валюте или баллах")

    class Meta:
        unique_together = ('hackathon', 'place')  # Уникальность места для каждого хакатона

    def __str__(self):
        return f"{self.place} место - {self.prize_amount or 0}"