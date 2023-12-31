# Generated by Django 4.2 on 2023-06-27 00:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("video", "0006_alter_detection_image_path"),
    ]

    operations = [
        migrations.AlterField(
            model_name="detection",
            name="detected_object",
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="detection",
            name="detected_time",
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name="detection",
            name="video",
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.CASCADE, to="video.video"
            ),
        ),
    ]
