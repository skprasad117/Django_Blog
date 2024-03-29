# Generated by Django 4.2.2 on 2023-06-19 11:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Response",
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
                ("post_id", models.CharField(max_length=20)),
                ("username", models.CharField(max_length=20)),
                ("like", models.BooleanField(default=False)),
                ("comment", models.CharField(blank=True, max_length=100)),
                ("first_response_date", models.DateTimeField(auto_now_add=True)),
                ("last_response_edit_date", models.DateTimeField(auto_now=True)),
                ("nested", models.BooleanField(blank=True, default=False)),
                (
                    "nested_response_id",
                    models.CharField(blank=True, default="", max_length=4),
                ),
                ("comment_flag", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="Posts",
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
                ("title", models.CharField(max_length=50)),
                ("content", models.CharField(max_length=500)),
                ("image", models.ImageField(default="", upload_to="blogs/images")),
                ("pub_date", models.DateTimeField(auto_now_add=True)),
                ("last_edit_date", models.DateTimeField(auto_now=True)),
                (
                    "author_name",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CommentsResponse",
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
                ("reaction", models.BooleanField(default=False)),
                ("response_flag", models.BooleanField(default=False)),
                (
                    "response",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to="blogs.response"
                    ),
                ),
                (
                    "user_name",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
