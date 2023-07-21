# Generated by Django 4.2.3 on 2023-07-21 06:54

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
            name="Employee",
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
                ("name", models.CharField(max_length=100)),
                ("position", models.CharField(max_length=100)),
                ("phone_number", models.CharField(max_length=20)),
                ("password", models.CharField(default="", max_length=100)),
                ("email", models.EmailField(max_length=254)),
                ("is_approved", models.BooleanField(default=False)),
                (
                    "user",
                    models.OneToOneField(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="InstagramPost",
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
                ("hashtag", models.CharField(max_length=100)),
                ("post_link", models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name="InstagramProfile",
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
                ("username", models.CharField(max_length=100)),
                ("verified", models.BooleanField(default=False)),
                ("followers", models.IntegerField(default=0)),
                ("following", models.IntegerField(default=0)),
                ("biography", models.TextField(blank=True, null=True)),
                ("post_urls", models.JSONField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="InstagramStats",
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
                ("post_link", models.URLField()),
                ("comments", models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name="SubredditData",
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
                ("subreddit_name", models.CharField(max_length=100)),
                ("selftext", models.TextField()),
                ("author_fullname", models.CharField(max_length=100)),
                ("title", models.CharField(max_length=200)),
                ("name", models.CharField(max_length=100)),
                ("upvote_ratio", models.FloatField()),
                ("score", models.IntegerField()),
                ("author", models.CharField(max_length=100)),
                ("subreddit_subscribers", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Manager",
            fields=[
                ("name", models.CharField(max_length=100)),
                (
                    "employee",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="manager",
                        serialize=False,
                        to="authentication.employee",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Team",
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
                ("name", models.CharField(max_length=100)),
                (
                    "manager",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="managed_team",
                        to="authentication.employee",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Request",
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
                ("is_approved", models.BooleanField(default=False)),
                (
                    "employee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="authentication.employee",
                    ),
                ),
            ],
        ),
    ]