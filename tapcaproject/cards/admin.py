from django.contrib import admin

from .models import Card, Tag


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('word', 'transcription', 'part_of_speech')
    list_editable = ('transcription', 'part_of_speech')
    search_fields = ('word', 'translation')


admin.site.register(Tag)
