# Generated by Django 4.2.1 on 2023-06-22 05:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("post", "0004_alter_post_content"),
    ]

    operations = [
        migrations.RenameField(
            model_name="post",
            old_name="content",
            new_name="post_content",
        ),
        migrations.RenameField(
            model_name="post",
            old_name="title",
            new_name="post_title",
        ),
    ]