# Generated by Django 4.1.7 on 2023-04-08 08:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="PaymentMethod",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("mask", models.CharField(max_length=4)),
                ("payment_method_id", models.UUIDField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payment_methods",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Tariff",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=255)),
                ("cost", models.DecimalField(decimal_places=2, max_digits=6)),
                (
                    "period_type",
                    models.CharField(
                        choices=[
                            ("week", "week"),
                            ("month", "month"),
                            ("year", "year"),
                        ],
                        default="month",
                        max_length=10,
                    ),
                ),
                ("description", models.TextField()),
                ("is_active", models.BooleanField(default=True)),
                ("trial_period", models.BooleanField(default=False)),
                (
                    "trial_period_type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("week", "week"),
                            ("month", "month"),
                            ("year", "year"),
                        ],
                        max_length=10,
                        null=True,
                    ),
                ),
                ("next_tariff_id", models.UUIDField(blank=True, null=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Subscription",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("ended_at", models.DateTimeField()),
                ("is_active", models.BooleanField(default=True)),
                ("is_waiting", models.BooleanField(default=False)),
                (
                    "payment_method",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="subscriptions",
                        to="billing.paymentmethod",
                    ),
                ),
                (
                    "tariff",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="subscriptions",
                        to="billing.tariff",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="subscriptions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Bill",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                (
                    "subscription",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="bills",
                        to="billing.subscription",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
