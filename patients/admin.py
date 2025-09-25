from django.contrib import admin
from .models import Patient, Banner

admin.site.register(Patient)

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'image', 'created_at')