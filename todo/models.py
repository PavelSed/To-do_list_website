# название
# форма
# описание
# статус важности
# отметка времени, когда запись была создана

from django.db import models
# Импортируем пользователя, который позволит нам создать модель
from django.contrib.auth.models import User

class Todo(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    # Связывает пользователя с моделью
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
