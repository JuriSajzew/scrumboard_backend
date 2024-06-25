import datetime
from django.conf import settings
from django.db import models


# Create your views here.
LOW = 'low'
MEDIUM = 'medium'
HIGH = 'high'
PRIORITY_CHOICES = [
    (LOW, 'Low'),
    (MEDIUM, 'Medium'),
    (HIGH, 'High'), 
]
class Todolist(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=150)
    created_at = models.DateField(default=datetime.date.today)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    priority = models.CharField(max_length=6, choices = PRIORITY_CHOICES, default = MEDIUM)
    dateline = models.DateField(null=True, blank=True)
    state = models.CharField(max_length=30, null=True, blank=True)
    
    def __str__(self):
        return f'{self.id} {self.title}'
