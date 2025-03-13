import json
from functools import wraps
from urllib.request import urlopen

from django.contrib.auth import authenticate
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.http import JsonResponse
from jose import jwt

from clerkproject import settings


class JwtAuthBackend(BaseBackend):
    def authenticate(self, request, **kwargs):
        if 'Authorization' not in request.headers:
            return None

        # Strip the "Bearer " prefix from the header
        token = request.headers['Authorization'][7:]

        if not token:
            raise None

        try:
            url = settings.CLERK_JWKS_URL
            response = urlopen(url)
            data_json = json.loads(response.read())
            decoded = jwt.decode(token, data_json['keys'][0], algorithms=['RS256'])
        except Exception:
            return None

        # Ideally at this point user object must be fetched from DB and returned, but we will just return a dummy
        # user object
        user = User(username=decoded['sub'], password="None")
        return user

    def get_user(self, user_id):
        return User(username=user_id, password="None")


def jwt_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = authenticate(request)
        if not user:
            return JsonResponse({'error': 'User not authenticated'}, status=401)
        request.user = user
        return view_func(request, *args, **kwargs)

    return _wrapped_view
