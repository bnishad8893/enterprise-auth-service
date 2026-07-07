"""Initial migration for PasswordResetToken model."""
from __future__ import annotations

from typing import ClassVar

from django.conf import settings
from django.db import migrations, models
from django.db.migrations.operations.base import Operation


class Migration(migrations.Migration):

    initial: ClassVar[bool] = True

    dependencies: ClassVar[list[tuple[str, str]]] = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations: ClassVar[list[Operation]] = [
        migrations.CreateModel(
            name="PasswordResetToken",
            fields=[
                (
                    "id",
                    models.UUIDField(primary_key=True, editable=False, auto_created=True),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        related_name="password_reset_tokens",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("hashed_token", models.CharField(max_length=128, db_index=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("expires_at", models.DateTimeField()),
                ("used_at", models.DateTimeField(blank=True, null=True)),
                ("is_used", models.BooleanField(default=False, db_index=True)),
            ],
            options={
                "db_table": "authentication_passwordresettoken",
            },
        ),
        migrations.AddIndex(
            model_name="passwordresettoken",
            index=models.Index(fields=["user"], name="authentication_pass_user_idx"),
        ),
    ]
