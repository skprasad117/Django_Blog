# Generated by Django 4.2.2 on 2023-06-15 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blogs", "0005_remove_posts_likes_count"),
    ]

    operations = [
        migrations.AlterField(
            model_name="response",
            name="post_id",
            field=models.CharField(max_length=20),
        ),
    ]