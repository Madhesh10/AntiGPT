from django.views.decorators.http import require_GET
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.conf import settings
import pathlib


def _make_json_safe(obj):
    """
    Convert common non-JSON types to JSON-safe representations.
    - Path -> string
    - tuple -> list
    - backend classes -> string
    - fallback -> string
    """
    if isinstance(obj, pathlib.Path):
        return str(obj)

    if isinstance(obj, (list, dict, str, int, float, bool)) or obj is None:
        return obj

    if isinstance(obj, tuple):
        return [_make_json_safe(x) for x in obj]

    # If it's a Django backend class, convert to dotted path
    try:
        module = obj.__module__
        name = obj.__class__.__name__
        return f"{module}.{name}"
    except Exception:
        pass

    # Try to iterate it
    try:
        return [_make_json_safe(x) for x in obj]
    except Exception:
        pass

    # Fallback to string
    return str(obj)


@require_GET
def diag_auth_view(request):
    User = get_user_model()

    # Make AUTHENTICATION_BACKENDS completely JSON-safe
    auth_backends = getattr(settings, "AUTHENTICATION_BACKENDS", None)
    if auth_backends:
        try:
            auth_backends = list(auth_backends)
        except Exception:
            auth_backends = str(auth_backends)

    result = {
        "DATABASE_ENGINE": settings.DATABASES.get("default", {}).get("ENGINE"),
        "DATABASE_NAME": settings.DATABASES.get("default", {}).get("NAME"),
        "AUTH_USER_MODEL": getattr(settings, "AUTH_USER_MODEL", "auth.User"),
        "AUTHENTICATION_BACKENDS": auth_backends,
        "DEBUG": settings.DEBUG,
    }

    try:
        result["users_count"] = User.objects.count()
        user = User.objects.filter(username="madhesh").first()
        result["madhesh_exists"] = bool(user)

        if user:
            result["madhesh_is_active"] = user.is_active
            result["madhesh_is_staff"] = user.is_staff
            result["madhesh_is_superuser"] = user.is_superuser
            result["madhesh_password_matches_madhesh123"] = user.check_password("madhesh123")
        else:
            result["madhesh_is_active"] = None
            result["madhesh_password_matches_madhesh123"] = False

    except Exception as e:
        result["db_error"] = str(e)

    # Convert all values to JSON-safe types
    safe_result = {k: _make_json_safe(v) for k, v in result.items()}

    return JsonResponse(safe_result)
