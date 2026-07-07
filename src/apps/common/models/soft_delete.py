"""Soft-delete mixin for Django models.

Provides a nullable `deleted_at` timestamp and helper methods to
perform soft-delete semantics while still allowing hard deletes.

Behaviour is intentionally minimal: state management lives on the model
and callers decide whether to filter out deleted rows at the query
layer (e.g. custom managers or repository patterns).
"""

from __future__ import annotations

from django.db import models
from django.utils import timezone


class SoftDeleteModel(models.Model):
    """Abstract model that adds `deleted_at` and helpers.

    Design decisions:
    - Keep soft-delete implementation lightweight and explicit.
    - Avoid overriding `delete()` so callers may still perform hard deletes
      when desired. Use `soft_delete()` and `restore()` for the usual flow.
    - Index `deleted_at` to make queries that exclude deleted rows efficient.
    """

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        default=None,
        db_index=True,
    )

    @property
    def is_deleted(self) -> bool:
        """Return whether the instance is soft-deleted.

        This is intentionally a simple property to keep checks explicit
        in domain code (instead of relying on implicit query filters).
        """

        return self.deleted_at is not None

    def soft_delete(self) -> None:
        if not self.is_deleted:
            self.deleted_at = timezone.now()
            self.save(update_fields=["deleted_at"])

    def restore(self) -> None:
        if self.is_deleted:
            self.deleted_at = None
            self.save(update_fields=["deleted_at"])

    class Meta:  # pragma: no cover - simple container
        abstract = True
