# antiGPTproject/urls.py
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.contrib.auth import get_user_model


# ==========================
# TEMPORARY — RESET ADMIN PASSWORD
# ==========================
def reset_admin_password_view(request):
    """
    Temporary endpoint:
    Creates user 'madhesh' if missing and sets password to 'madhesh123'.
    Gives admin/superuser rights.

    Visit once:
        https://antigpt-v15z.onrender.com/reset-admin-password/

    REMOVE THIS AFTER LOGIN WORKS.
    """
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
            return HttpResponse(
                f"Created user '{username}' and set password to '{new_password}'."
            )
        return HttpResponse(
            f"Updated password for existing user '{username}' to '{new_password}'."
        )

    except Exception as e:
        return HttpResponse(f"ERROR: {e}", status=500)


# ==========================
# URL patterns
# ==========================
urlpatterns = [
    path("admin/", admin.site.urls),

    # TEMP: Reset admin password endpoint
    path("reset-admin-password/", reset_admin_password_view),

    # App URLs
    path("", include("accounts.urls")),
    path("", include("chatbot.urls")),
]
