# Generated by Django 4.2.1 on 2023-06-21 02:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("video", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Detection",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("latitude", models.FloatField()),
                ("longitude", models.FloatField()),
                ("timestamp", models.DateTimeField()),
                ("detected_object", models.IntegerField()),
                ("image_path", models.CharField(max_length=200)),
                ("frame", models.IntegerField()),
                (
                    "video",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="video.video"
                    ),
                ),
            ],
        ),
    ]