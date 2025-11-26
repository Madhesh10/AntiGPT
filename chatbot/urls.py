from django.urls import path
from . import views

urlpatterns = [
    path('', views.conversations, name='conversations'),
    path('conversation/<int:pk>/', views.conversation_detail, name='conversation_detail'),
    path('conversation/<int:pk>/add/', views.add_message, name='add_message'),
]
