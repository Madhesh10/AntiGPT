from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chatbot.urls')),  # Chat system pages
    path('', include('accounts.urls')), # Login/Signup system
]
