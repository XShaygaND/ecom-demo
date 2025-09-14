# ecommerce/users/backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailAuthBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        email = username

        if not email:
            email = kwargs.get("email") or kwargs.get("username")

        if not email and request is not None:
            data = getattr(request, "data", None)
            if data:
                email = data.get("email") or data.get("username")
            else:
                email = request.POST.get("email") or request.POST.get("username")

        if not email or not password:
            return None

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None
