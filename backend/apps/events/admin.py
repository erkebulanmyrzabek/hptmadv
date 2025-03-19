from django.contrib import admin
from .models import Hackathon, HackathonOrganizer, HackathonJudge, HackathonScheduleEvent, HackathonRules, Participant, Team, Track
# Inline для Организаторов
class OrganizerInline(admin.TabularInline):
    model = HackathonOrganizer
    extra = 1  # Количество пустых форм для добавления новых организаторов

# Inline для Судей
class JudgeInline(admin.TabularInline):
    model = HackathonJudge
    extra = 1

# Inline для Расписания
class ScheduleEventInline(admin.TabularInline):
    model = HackathonScheduleEvent
    extra = 1

# Inline для Правил
class HackathonRulesInline(admin.TabularInline):
    model = HackathonRules
    extra = 1

# Inline для Участников
class ParticipantInline(admin.TabularInline):
    model = Participant
    extra = 1
    readonly_fields = ('name', 'role', 'stack', 'team')  # Участники только для просмотра
    can_delete = False  # Запрещаем удаление участников из админки

# Inline для Команд
class TeamInline(admin.TabularInline):
    model = Team
    extra = 1
    readonly_fields = ('name', 'stack', 'status', 'max_members', 'invite_code')  # Команды только для просмотра
    can_delete = False  # Запрещаем удаление команд из админки

# Inline для Треков
class TrackInline(admin.TabularInline):
    model = Track
    extra = 1

# Админка для Hackathon
@admin.register(Hackathon)
class HackathonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'start_date', 'end_date', 'location')
    list_filter = ('status', 'start_date')
    search_fields = ('title', 'location')
    inlines = [
        OrganizerInline,
        JudgeInline,
        ScheduleEventInline,
        HackathonRulesInline,
        ParticipantInline,
        TeamInline,
        TrackInline,
    ]

# Регистрация остальных моделей (для доступа через боковое меню)
@admin.register(HackathonOrganizer)
class OrganizerAdmin(admin.ModelAdmin):
    list_display = ('name', 'hackathon')
    list_filter = ('hackathon',)

@admin.register(HackathonJudge)
class JudgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'hackathon')
    list_filter = ('hackathon',)

@admin.register(HackathonScheduleEvent)
class ScheduleEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'time', 'hackathon')
    list_filter = ('hackathon', 'time')

@admin.register(HackathonRules)
class HackathonRulesAdmin(admin.ModelAdmin):
    list_display = ('text', 'hackathon')
    list_filter = ('hackathon',)

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'team', 'hackathon')
    list_filter = ('hackathon', 'team')
    search_fields = ('name',)

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'invite_code', 'hackathon')
    list_filter = ('hackathon', 'status')
    search_fields = ('name', 'invite_code')

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('title', 'hackathon', 'teams_count', 'participants_count')
    list_filter = ('hackathon',)

    def teams_count(self, obj):
        return obj.teams_count()
    teams_count.short_description = 'Количество команд'

    def participants_count(self, obj):
        return obj.participants_count()
    participants_count.short_description = 'Количество участников'