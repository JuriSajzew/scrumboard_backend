import datetime
from django.conf import settings
from django.db import models


# Create your views here.

class Todolist(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=150)
    created_at = models.DateField(default=datetime.date.today)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    
    
    def __str__(self):
        return f'{self.id} {self.title}'
