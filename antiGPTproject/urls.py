# antiGPTproject/urls.py
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from .create_admin import run as create_admin_run

def create_admin_view(request):
    created = create_admin_run()
    if created:
        return HttpResponse("Admin user created. Username: madhesh / Password: madhesh123")
    return HttpResponse("Admin user already exists.")

urlpatterns = [
    path("admin/", admin.site.urls),

    # Temporary route to create an admin without shell access (remove after use)
    path("create-admin/", create_admin_view),

    # Include your app URLconfs. Order: accounts first so /login/ is available,
    # and then chatbot (so root and other app routes work).
    path("", include("accounts.urls")),
    path("", include("chatbot.urls")),
]
