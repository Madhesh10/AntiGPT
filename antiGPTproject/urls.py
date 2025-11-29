# antiGPTproject/urls.py
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.contrib.auth import get_user_model

# diagnostic view (make sure antiGPTproject/diag_auth.py exists)
from .diag_auth import diag_auth_view


def reset_admin_password_view(request):
    """
    Temporary: create user 'madhesh' if missing and set password to 'madhesh123'.
    Visit once, then remove this code and redeploy.
    """
    User = get_user_model()
    username = "madhesh"
    new_password = "madhesh123"
    try:
        user, created = User.objects.get_or_create(username=username, defaults={"email": ""})
        user.set_password(new_password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        if created:
            return HttpResponse(f"Created user {username} and set password to '{new_password}'.")
        return HttpResponse(f"Updated password for existing user {username} to '{new_password}'.")
    except Exception as e:
        return HttpResponse(f"Error: {e}", status=500)


urlpatterns = [
    # admin
    path("admin/", admin.site.urls),

    # TEMP endpoints: use once then REMOVE for security
    path("reset-admin-password/", reset_admin_password_view),
    path("diag-auth/", diag_auth_view),

    # application routes (accounts first so /login/ resolves)
    path("", include("accounts.urls")),
    path("", include("chatbot.urls")),
]
