from django.urls import path

from api.views import get_questions

app_name = 'api'

urlpatterns = [
    path('post/', get_questions, name='post'),
]
