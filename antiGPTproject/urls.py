from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chatbot.urls')),  # Chat system pages
    path('', include('accounts.urls')), # Login/Signup system
]
from django.http import HttpResponse
from .create_admin import run as create_admin_run

def create_admin_view(request):
    create_admin_run()
    return HttpResponse("Admin user created successfully!")

urlpatterns = [
    # ... your existing paths
    path("create-admin/", create_admin_view),
]
