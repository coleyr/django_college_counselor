# Generated by Django 3.2.13 on 2022-08-19 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20220819_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counselor',
            name='img',
            field=models.ImageField(blank=True, default='/img/student-icon.png', upload_to='img'),
        ),
        migrations.AlterField(
            model_name='parent',
            name='img',
            field=models.ImageField(blank=True, default='/img/student-icon.png', upload_to='img'),
        ),
        migrations.AlterField(
            model_name='student',
            name='img',
            field=models.ImageField(blank=True, default='/img/student-icon.png', upload_to='img'),
        ),
    ]