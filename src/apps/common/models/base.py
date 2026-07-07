"""Composed base model used throughout the domain.

This model composes the small abstract mixins into a single building
block for most domain entities. It keeps model inheritance shallow and
explicit while providing a consistent set of fields across the project.
"""

from __future__ import annotations

from .soft_delete import SoftDeleteModel
from .timestamp import TimestampModel
from .uuid import UUIDModel


class BaseModel(UUIDModel, TimestampModel, SoftDeleteModel):
    """Base abstract model that composes UUID, timestamp and soft-delete.

    Keep this model abstract: concrete entities should inherit from it to
    get the common fields. Business logic should live in domain services
    or managers, not here.
    """

    class Meta:  # pragma: no cover - simple container
        abstract = True
