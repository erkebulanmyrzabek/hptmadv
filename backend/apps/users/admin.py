from django.contrib import admin
from .models import Participant, Skill, Certificate, Achievement

# Register your models here.


admin.site.register(Participant)
admin.site.register(Skill)
admin.site.register(Certificate)
admin.site.register(Achievement)

