# antiGPTproject/urls.py

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from .diag_auth import diag_auth_view   # <- make sure this file exists

# --- TEMP ADMIN PASSWORD RESET ---
def reset_admin_password_view(request):
    User = get_user_model()
    username = "madhesh"
    password = "madhesh123"

    user, created = User.objects.get_or_create(
        username=username,
        defaults={"email": ""}
    )
    user.set_password(password)
    user.is_staff = True
    user.is_superuser = True
    user.save()

    if created:
        return HttpResponse(f"Created user {username} with password {password}")
    return HttpResponse(f"Updated password for {username} to {password}")

# --- URL PATTERNS (IMPORTANT: must be a LIST, not a module!) ---
urlpatterns = [
    path("admin/", admin.site.urls),

    # Temporary admin fix URLs
    path("reset-admin-password/", reset_admin_password_view),
    path("diag-auth/", diag_auth_view),

    # App routes
    path("", include("accounts.urls")),
    path("", include("chatbot.urls")),
]
