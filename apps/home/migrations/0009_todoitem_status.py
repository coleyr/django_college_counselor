# Generated by Django 3.2.13 on 2022-09-10 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_alter_todoitem_todo_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='todoitem',
            name='status',
            field=models.CharField(choices=[('Not Being Worked on', 'NOT BEING WORKED ON'), ('In Progress', 'IN PROGRESS'), ('Awaiting Feedback', 'AWAITING FEEDBACK'), ('Complete', 'COMPLETE'), ('stuck', 'STUCK')], default='Not Being Worked on', max_length=20),
        ),
    ]
