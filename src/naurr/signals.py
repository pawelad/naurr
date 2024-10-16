"""naurr app signals."""

from collections.abc import Callable
from typing import Any

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(
    sender: Callable,
    instance: get_user_model() | None = None,
    created: bool = False,
    **kwargs: Any,
) -> None:
    """Create API auth token after user is created."""
    if created:
        Token.objects.create(user=instance)
