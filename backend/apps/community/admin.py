from django.contrib import admin

# Register your models here.
from .models import Team

print("Registering Team model in admin...")  # Добавляем отладочный print

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'hackathon', 'created_at')
    search_fields = ('name', 'hackathon__title')
    list_filter = ('hackathon__title',)

admin.site.register(Team, TeamAdmin)
print("Team model registered in admin!")  # Добавляем отладочный print
