from django.contrib import admin
from .models import AdminAction, AdminConfig

admin.site.register(AdminAction)
admin.site.register(AdminConfig)