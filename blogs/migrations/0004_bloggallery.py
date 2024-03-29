# Generated by Django 4.2.2 on 2023-06-20 07:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("blogs", "0003_remove_commentsresponse_response_flag"),
    ]

    operations = [
        migrations.CreateModel(
            name="BlogGallery",
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
                ("images", models.ImageField(upload_to="blog/gallery")),
                ("upload_date", models.DateField(auto_now_add=True)),
                (
                    "blog",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="blogs.response"
                    ),
                ),
            ],
        ),
    ]
