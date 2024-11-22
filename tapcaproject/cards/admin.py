from django.contrib import admin

from .models import Card, Tag, Form, Example


class FormsInline(admin.TabularInline):
    model = Form
    extra = 5


class ExampleInline(admin.TabularInline):
    model = Example
    extra = 10


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('word', 'transcription', 'part_of_speech')
    list_editable = ('transcription', 'part_of_speech')
    search_fields = ('word', 'translation')

    inlines = (FormsInline, ExampleInline,)

admin.site.register(Tag)



