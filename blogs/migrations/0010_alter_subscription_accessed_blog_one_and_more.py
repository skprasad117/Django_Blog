# Generated by Django 4.2.2 on 2023-06-21 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blogs", "0009_subscription_accessed_blog_one_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subscription",
            name="accessed_blog_one",
            field=models.IntegerField(blank=True, default=None),
        ),
        migrations.AlterField(
            model_name="subscription",
            name="accessed_blog_two",
            field=models.IntegerField(blank=True, default=None),
        ),
    ]
