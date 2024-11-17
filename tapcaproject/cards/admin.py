from django.contrib import admin

from .models import Card


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('word', 'transcription', 'translation')
    list_editable = ('transcription', 'translation')
    search_fields = ('word', 'translation')
