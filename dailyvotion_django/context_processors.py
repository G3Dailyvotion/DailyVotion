"""Custom context processors for the DailyVotion project."""

from __future__ import annotations

from django.conf import settings


def static_version(request):  # pragma: no cover - trivial
    """Expose a STATIC_VERSION value to templates for cache busting.

    The value can be overridden via the environment variable STATIC_VERSION.
    Falls back to a date-like default so that if not set it is still stable.
    """
    return {"STATIC_VERSION": getattr(settings, "STATIC_VERSION", "v1")}
