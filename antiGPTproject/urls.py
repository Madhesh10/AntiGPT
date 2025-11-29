# antiGPTproject/urls.py  -- diagnostic edition (temporary)
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db import connection
import json

# TEMP: reset admin password (keeps your previous reset behaviour)
def reset_admin_password_view(request):
    User = get_user_model()
    username = "madhesh"
    new_password = "madhesh123"
    try:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={"email": ""}
        )
        user.set_password(new_password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        if created:
            return HttpResponse(f"Created user '{username}' and set password to '{new_password}'.")
        return HttpResponse(f"Updated password for existing user '{username}' to '{new_password}'.")
    except Exception as e:
        return HttpResponse(f"ERROR: {e}", status=500)

# DIAGNOSTIC endpoint to inspect auth state
def diag_auth_view(request):
    out = {}
    try:
        # basic settings
        out["DEBUG"] = bool(getattr(settings, "DEBUG", False))
        out["AUTH_USER_MODEL"] = getattr(settings, "AUTH_USER_MODEL", "auth.User (default)")
        out["AUTHENTICATION_BACKENDS"] = list(getattr(settings, "AUTHENTICATION_BACKENDS", []))

        # DB info (default)
        default_db = settings.DATABASES.get("default", {})
        out["DATABASE_ENGINE"] = default_db.get("ENGINE")
        out["DATABASE_NAME"] = default_db.get("NAME")

        # connection info
        out["db_is_connected"] = connection is not None

        # user info
        User = get_user_model()
        try:
            users_count = User.objects.count()
        except Exception as e:
            users_count = f"EXCEPTION: {e}"
        out["users_count"] = users_count

        # existence and password check for madhesh
        username = "madhesh"
        try:
            user = User.objects.filter(username=username).first()
            if not user:
                out["madhesh_exists"] = False
                out["madhesh_password_matches"] = False
                out["madhesh_password_hash"] = None
            else:
                out["madhesh_exists"] = True
                # do NOT expose full hash in production; we show only the algorithm prefix and length
                ph = getattr(user, "password", "")
                out["madhesh_password_hash_preview"] = ph[:60] + ("..." if len(ph) > 60 else "")
                # check password
                out["madhesh_password_matches"] = user.check_password("madhesh123")
                out["madhesh_is_superuser"] = bool(getattr(user, "is_superuser", False))
                out["madhesh_is_staff"] = bool(getattr(user, "is_staff", False))
        except Exception as e:
            out["madhesh_check_exception"] = str(e)
    except Exception as e:
        return HttpResponse(f"DIAG ERROR: {e}", status=500)

    # render JSON for clarity
    return HttpResponse(json.dumps(out, indent=2), content_type="application/json")


urlpatterns = [
    path("admin/", admin.site.urls),

    # TEMP endpoints (remove after diagnostics)
    path("reset-admin-password/", reset_admin_password_view),
    path("diag-auth/", diag_auth_view),

    # your app includes
    path("", include("accounts.urls")),
    path("", include("chatbot.urls")),
]
