# Generated by Django 3.1.2 on 2021-11-04 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("english", "0005_auto_20211101_1402"),
    ]

    operations = [
        migrations.AddField(
            model_name="wordparams",
            name="english",
            field=models.BooleanField(default=False),
        ),
    ]
