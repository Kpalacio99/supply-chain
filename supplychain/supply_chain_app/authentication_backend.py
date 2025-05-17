from django.contrib.auth.backends import BaseBackend
from .models import CustomUser

class CustomAuthenticationBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = CustomUser.objects.get(username=username)
            if user.password == password:  # Remember to hash passwords in production
                return user
        except CustomUser.DoesNotExist:
            return None
