# Generated by Django 3.1.2 on 2022-03-14 08:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('english', '0013_auto_20220311_2155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='words',
            name='control_list',
            field=models.ManyToManyField(blank=True, related_name='user_control', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='words',
            name='heavy_list',
            field=models.ManyToManyField(blank=True, related_name='user_heavy', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='words',
            name='learned_list',
            field=models.ManyToManyField(blank=True, related_name='user_learned', to=settings.AUTH_USER_MODEL),
        ),
    ]
