from django.db import models
from django.core.exceptions import ValidationError

class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    telegram = models.URLField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name