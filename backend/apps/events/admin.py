from django.contrib import admin
from .models import Hackathon, HackathonDetails, HackathonSchedule, HackathonLocation, HackathonParticipants, Tag, HackathonPrizePlace


class HackathonDetailsInline(admin.StackedInline):
    model = HackathonDetails
    can_delete = False


class HackathonScheduleInline(admin.StackedInline):
    model = HackathonSchedule
    can_delete = False


class HackathonLocationInline(admin.StackedInline):
    model = HackathonLocation
    can_delete = False


class HackathonParticipantsInline(admin.StackedInline):
    model = HackathonParticipants
    can_delete = False


class HackathonPrizePlaceInline(admin.TabularInline):
    model = HackathonPrizePlace
    extra = 1


@admin.register(Hackathon)
class HackathonAdmin(admin.ModelAdmin):
    inlines = [
        HackathonDetailsInline,
        HackathonScheduleInline,
        HackathonLocationInline,
        HackathonParticipantsInline,
        HackathonPrizePlaceInline,
    ]
    list_display = ('title', 'organization', 'status', 'type', 'created_at')
    list_filter = ('status', 'type', 'organization')
    search_fields = ('title',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)