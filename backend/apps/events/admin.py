from django.contrib import admin
from .models import Event, Hackathon, Organization, Tag, HackathonPrizePlace

class HackathonPrizePlaceInline(admin.TabularInline):
    model = HackathonPrizePlace
    extra = 1  # Показывать одну пустую форму по умолчанию
    min_num = 1  # Минимум одно призовое место
    fields = ('place', 'prize_amount')

class HackathonInline(admin.StackedInline):
    model = Hackathon
    extra = 0
    can_delete = False
    inlines = [HackathonPrizePlaceInline]  # Вложенная инлайн-форма для призовых мест

class EventAdmin(admin.ModelAdmin):
    list_display = ('event_type', 'organization', 'created_at')
    list_filter = ('event_type',)
    search_fields = ('organization__name',)

    inlines = []

    def get_inlines(self, request, obj):
        if obj and obj.event_type == 'hackathon':
            return [HackathonInline]
        return []

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.event_type == 'hackathon' and not hasattr(obj, 'hackathon'):
            Hackathon.objects.create(event=obj, title=f"{obj.organization} Hackathon")

admin.site.register(Event, EventAdmin)
admin.site.register(Organization)
admin.site.register(Tag)