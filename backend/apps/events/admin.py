from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from .models import Hackathon, Tag, Organization, HackathonPrizePlace
from django.contrib.admin import TabularInline
from django.contrib import messages

class PrizePlacesInline(TabularInline):
    model = HackathonPrizePlace
    extra = 1
    fields = ('place', 'number_of_winners', 'prize_amount', 'xp_reward')

@admin.register(Hackathon)
class HackathonAdmin(admin.ModelAdmin):
    inlines = [PrizePlacesInline]
    list_display = ['title', 'status', 'type', 'registration_start_date', 'end_date']
    list_filter = ['status', 'type', 'registration_start_date', 'end_date']
    search_fields = ['title', 'short_description', 'full_description']
    filter_horizontal = ['tags', 'participants']
    fieldsets = (
        ('Основная информация', {
            'fields': ('organization', 'title', 'short_description', 'full_description', 'preview_image', 'banner_image')
        }),
        ('Статус и тип', {
            'fields': ('status', 'type')
        }),
        ('Даты', {
            'fields': ('registration_start_date', 'registration_end_date', 'start_date', 'end_date')
        }),
        ('Место проведения', {
            'fields': ('location', 'address')
        }),
        ('Участники', {
            'fields': ('participants', 'max_participants')
        }),
        ('Дополнительно', {
            'fields': ('tags', 'faq', 'rules')
        }),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.update_participants_count()

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['name']

@admin.register(HackathonPrizePlace)
class HackathonPrizePlaceAdmin(admin.ModelAdmin):
    list_display = ['hackathon', 'place', 'number_of_winners', 'prize_amount', 'xp_reward', 'current_winners_count']
    list_filter = ['place', 'hackathon']
    search_fields = ['hackathon__title']
    filter_horizontal = ['winners', 'winner_teams']
    actions = ['distribute_rewards_action']
    fieldsets = (
        ('Основная информация', {
            'fields': ('hackathon', 'place', 'number_of_winners')
        }),
        ('Награды', {
            'fields': ('prize_amount', 'xp_reward')
        }),
        ('Победители', {
            'fields': ('winners', 'winner_teams')
        }),
    )

    def current_winners_count(self, obj):
        return obj.winners.count() + obj.winner_teams.count()
    current_winners_count.short_description = 'Количество победителей'

    def distribute_rewards_action(self, request, queryset):
        for prize_place in queryset:
            try:
                prize_place.distribute_rewards()
                self.message_user(
                    request,
                    f'Успешно распределены награды для {prize_place}',
                    messages.SUCCESS
                )
            except Exception as e:
                self.message_user(
                    request,
                    f'Ошибка при распределении наград для {prize_place}: {str(e)}',
                    messages.ERROR
                )
    distribute_rewards_action.short_description = 'Распределить награды выбранным призовым местам'
