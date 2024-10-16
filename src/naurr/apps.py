"""naurr app config."""

from django.apps import AppConfig


class NaurrConfig(AppConfig):
    """Django `AppConfig` integration for `naurr` app."""

    name = "naurr"
    verbose_name = "Naurr"

    def ready(self) -> None:
        """Import signals when the ap is ready."""
        from naurr import signals  # noqa
