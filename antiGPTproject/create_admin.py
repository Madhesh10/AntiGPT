# antiGPTproject/create_admin.py
from django.contrib.auth import get_user_model

def run():
    User = get_user_model()
    username = "madhesh"
    password = "madhesh123"
    email = ""

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
        return True
    return False
