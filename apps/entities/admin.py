from .models import Party
from django.contrib import admin

@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ("id", "entity", "role")
    list_filter = ("role",)
    search_fields = ("entity__name", "id")
    ordering = ("entity__name",)
