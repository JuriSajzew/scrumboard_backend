# Generated by Django 5.0.6 on 2024-06-25 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todolist', '0003_todolist_dateline'),
    ]

    operations = [
        migrations.AddField(
            model_name='todolist',
            name='state',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]