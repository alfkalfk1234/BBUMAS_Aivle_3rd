# Generated by Django 4.2.1 on 2023-07-03 01:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("post", "0004_alter_post_report_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="post_region",
            field=models.CharField(default=" ", max_length=150),
        ),
    ]
