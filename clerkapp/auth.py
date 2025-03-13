import json
from urllib.request import urlopen

from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework.exceptions import NotAuthenticated
from jose import jwt

from clerkproject import settings


class JwtAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):

        if 'Authorization' not in request.headers:
            raise NotAuthenticated('No token provided')

        # Strip the "Bearer " prefix from the header
        token = request.headers['Authorization'][7:]

        if not token:
            raise NotAuthenticated('No token provided')

        try:
            url = settings.CLERK_JWKS_URL
            response = urlopen(url)
            data_json = json.loads(response.read())
            decoded = jwt.decode(token, data_json['keys'][0], algorithms=['RS256'])
        except Exception:
            raise NotAuthenticated('Invalid token')

        # Ideally at this point user object must be fetched from DB and returned, but we will just return a dummy
        # user object
        user = User(username=decoded['sub'], password="None")
        return user, None

    def authenticate_header(self, request):
        # By default, if Authorization header is present Django maps the exception to 403 Forbidden This method makes
        # DRF return 401 with WWW-Authenticate header, This is optional though if you are okay with 403
        return 'Bearer realm="api"'
