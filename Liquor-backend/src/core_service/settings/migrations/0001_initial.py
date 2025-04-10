# Generated by Django 4.2.10 on 2025-03-25 16:51

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SystemSetting",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "key",
                    models.CharField(max_length=100, unique=True, verbose_name="key"),
                ),
                ("value", models.TextField(verbose_name="value")),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="description"),
                ),
                (
                    "is_public",
                    models.BooleanField(default=False, verbose_name="is public"),
                ),
            ],
            options={
                "verbose_name": "system setting",
                "verbose_name_plural": "system settings",
                "ordering": ["key"],
            },
        ),
        migrations.CreateModel(
            name="TenantSetting",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("tenant_id", models.UUIDField(db_index=True)),
                ("key", models.CharField(max_length=100, verbose_name="key")),
                ("value", models.TextField(verbose_name="value")),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="description"),
                ),
            ],
            options={
                "verbose_name": "tenant setting",
                "verbose_name_plural": "tenant settings",
                "ordering": ["key"],
                "unique_together": {("tenant_id", "key")},
            },
        ),
        migrations.CreateModel(
            name="NotificationTemplate",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("tenant_id", models.UUIDField(db_index=True)),
                ("name", models.CharField(max_length=100, verbose_name="name")),
                ("title", models.CharField(max_length=255, verbose_name="title")),
                ("body", models.TextField(verbose_name="body")),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="description"),
                ),
            ],
            options={
                "verbose_name": "notification template",
                "verbose_name_plural": "notification templates",
                "ordering": ["name"],
                "unique_together": {("tenant_id", "name")},
            },
        ),
        migrations.CreateModel(
            name="EmailTemplate",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                ("tenant_id", models.UUIDField(db_index=True)),
                ("name", models.CharField(max_length=100, verbose_name="name")),
                ("subject", models.CharField(max_length=255, verbose_name="subject")),
                ("body", models.TextField(verbose_name="body")),
                (
                    "description",
                    models.TextField(blank=True, verbose_name="description"),
                ),
            ],
            options={
                "verbose_name": "email template",
                "verbose_name_plural": "email templates",
                "ordering": ["name"],
                "unique_together": {("tenant_id", "name")},
            },
        ),
    ]
