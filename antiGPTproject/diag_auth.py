# antiGPTproject/diag_auth.py
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.conf import settings

def _make_json_safe(obj):
    import pathlib
    if isinstance(obj, pathlib.Path):
        return str(obj)
    if isinstance(obj, (list, dict, str, int, float, bool)) or obj is None:
        return obj
    if isinstance(obj, tuple):
        return [ _make_json_safe(x) for x in obj ]
    try:
        iter(obj)
    except TypeError:
        return str(obj)
    try:
        return [ _make_json_safe(x) for x in obj ]
    except Exception:
        return str(obj)

@require_GET
def diag_auth_view(request):
    User = get_user_model()
    result = {
        "DATABASE_ENGINE": settings.DATABASES.get("default", {}).get("ENGINE"),
        "DATABASE_NAME": settings.DATABASES.get("default", {}).get("NAME"),
        "AUTH_USER_MODEL": getattr(settings, "AUTH_USER_MODEL", "auth.User"),
        "AUTHENTICATION_BACKENDS": getattr(settings, "AUTHENTICATION_BACKENDS", None),
        "DEBUG": getattr(settings, "DEBUG", None),
    }

    try:
        result["users_count"] = User.objects.count()
        user = User.objects.filter(username="madhesh").first()
        result["madhesh_exists"] = bool(user)
        if user:
            result["madhesh_is_active"] = getattr(user, "is_active", None)
            result["madhesh_is_staff"] = getattr(user, "is_staff", None)
            result["madhesh_is_superuser"] = getattr(user, "is_superuser", None)
            result["madhesh_password_matches_madhesh123"] = user.check_password("madhesh123")
        else:
            result["madhesh_is_active"] = None
            result["madhesh_password_matches_madhesh123"] = False
    except Exception as e:
        result["db_error"] = str(e)

    safe_result = {k: _make_json_safe(v) for k, v in result.items()}
    return JsonResponse(safe_result)
