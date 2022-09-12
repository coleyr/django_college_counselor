# Generated by Django 3.2.13 on 2022-09-10 18:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_todoitem_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todolist',
            name='assignee',
        ),
        migrations.AddField(
            model_name='todoitem',
            name='assignee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]