# Generated by Django 2.0.7 on 2018-07-28 13:51

from django.db import migrations, models
import jsonfield.encoder
import jsonfield.fields
import sberbank.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="LogEntry",
            fields=[
                ("uid", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("payment_id", models.UUIDField(blank=True, db_index=True, null=True, verbose_name="payment ID")),
                ("bank_id", models.UUIDField(blank=True, db_index=True, null=True, verbose_name="bank payment ID")),
                (
                    "request_type",
                    models.CharField(
                        choices=[(0, "CREATE"), (1, "CALLBACK"), (2, "CHECK_STATUS")],
                        db_index=True,
                        max_length=1,
                        verbose_name="request type",
                    ),
                ),
                ("response_text", models.TextField(blank=True, null=True, verbose_name="response text")),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="created")),
                ("checksum", models.CharField(blank=True, db_index=True, max_length=256, null=True)),
            ],
            options={
                "ordering": ["-created"],
            },
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                ("uid", models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ("bank_id", models.UUIDField(blank=True, db_index=True, null=True, verbose_name="bank ID")),
                ("amount", models.DecimalField(decimal_places=2, max_digits=128, verbose_name="amount")),
                ("error_code", models.PositiveIntegerField(blank=True, null=True, verbose_name="error code")),
                ("error_message", models.TextField(blank=True, null=True, verbose_name="error message")),
                (
                    "status",
                    models.PositiveSmallIntegerField(
                        choices=[(0, "CREATED"), (1, "PENDING"), (2, "SUCCEEDED"), (3, "FAILED")],
                        db_index=True,
                        default=sberbank.models.Status(0),
                        verbose_name="status",
                    ),
                ),
                (
                    "details",
                    jsonfield.fields.JSONField(
                        blank=True,
                        dump_kwargs={"cls": jsonfield.encoder.JSONEncoder, "separators": (",", ":")},
                        load_kwargs={},
                        null=True,
                        verbose_name="details",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="created")),
                ("updated", models.DateTimeField(auto_now=True, db_index=True, verbose_name="modified")),
            ],
            options={
                "verbose_name": "payment",
                "ordering": ["-updated"],
                "verbose_name_plural": "payments",
            },
        ),
    ]
