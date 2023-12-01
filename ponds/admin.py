from django.contrib import admin
from .models import Farm, Pond


class FarmAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_editable = ['name',]

admin.site.register(Farm, FarmAdmin)


class PondAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_editable = ['name',]

admin.site.register(Pond, PondAdmin)
