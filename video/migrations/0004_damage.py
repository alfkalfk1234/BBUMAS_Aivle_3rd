# Generated by Django 4.2 on 2023-06-23 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("video", "0003_detection_is_checked"),
    ]

    operations = [
        migrations.CreateModel(
            name="Damage",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("time", models.DateTimeField()),
                ("latitude", models.FloatField()),
                ("longitude", models.FloatField()),
                ("department", models.CharField(max_length=100)),
                ("imaga_name", models.CharField(max_length=100)),
            ],
        ),
    ]
