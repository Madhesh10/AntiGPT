# antiGPTproject/urls.py
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_GET

# Temporary endpoint to create/reset the admin user.
def reset_admin_password_view(request):
    """
    Creates user 'madhesh' if missing and sets password to 'madhesh123'.
    Visit once, then remove this code and redeploy.
    """
    User = get_user_model()
    username = "madhesh"
    new_password = "madhesh123"
    try:
        user, created = User.objects.get_or_create(username=username, defaults={"email": ""})
        user.set_password(new_password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()
        if created:
            return HttpResponse(f"Created user {username} and set password to '{new_password}'.")
        return HttpResponse(f"Updated password for existing user {username} to '{new_password}'.")
    except Exception as e:
        return HttpResponse(f"Error: {e}", status=500)


# Diagnostic endpoint to inspect auth DB state (read-only, safe)
@require_GET
def diag_auth_view(request):
    """
    Returns JSON with basic diagnostics:
      - auth_user table count
      - whether user 'madhesh' exists
      - whether password check succeeds (server-side)
      - AUTH_USER_MODEL and AUTHENTICATION_BACKENDS info (from settings)
    """
    from django.db import connection
    from django.conf import settings
    User = get_user_model()

    result = {
        "DATABASE_ENGINE": settings.DATABASES.get("default", {}).get("ENGINE"),
        "AUTH_USER_MODEL": getattr(settings, "AUTH_USER_MODEL", "auth.User"),
        "AUTHENTICATION_BACKENDS": getattr(settings, "AUTHENTICATION_BACKENDS", None),
        "DEBUG": getattr(settings, "DEBUG", None),
    }

    try:
        # Count users (safe)
        result["users_count"] = User.objects.count()
        try:
            user = User.objects.filter(username="madhesh").first()
            result["madhesh_exists"] = bool(user)
            if user:
                # check password server-side
                result["madhesh_is_active"] = getattr(user, "is_active", None)
                result["madhesh_is_staff"] = getattr(user, "is_staff", None)
                result["madhesh_is_superuser"] = getattr(user, "is_superuser", None)
                result["madhesh_password_matches_madhesh123"] = user.check_password("madhesh123")
            else:
                result["madhesh_is_active"] = None
                result["madhesh_password_matches_madhesh123"] = False
        except Exception as e:
            result["user_check_error"] = str(e)
    except Exception as e:
        # If the DB isn't ready or migrations missing, include error text
        result["db_error"] = str(e)

    return JsonResponse(result)
    

urlpatterns = [
    path("admin/", admin.site.urls),

    # TEMP: reset/create the admin password (visit once)
    path("reset-admin-password/", reset_admin_password_view),

    # TEMP diagnostic endpoint (GET only)
    path("diag-auth/", diag_auth_view),

    # your existing app includes
    path("", include("accounts.urls")),
    path("", include("chatbot.urls")),
]
