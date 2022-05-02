from django.db import models


class Requests(models.Model):
    id_req = models.PositiveIntegerField(
        'ID',)
    text_answer = models.CharField(
        'Текст ответа',
        max_length=500,)
    text_question = models.CharField(
        'Текст вопроса',
        max_length=500)
    created_at = models.DateTimeField(
        'Дата создания вопроса')

    class Meta:
        verbose_name = 'Запрос'
        verbose_name_plural = 'Запросы'

    def __str__(self):
        return self.text_question
