from django.contrib import admin

from .models import Requests


@admin.register(Requests)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'id_req', 'text_answer', 'text_question',
        'created_at',)
    search_fields = (
        'text_answer', 'text_question',)
    list_filter = ('id_req', 'text_answer',)
    empty_value_display = '-Empty-'
