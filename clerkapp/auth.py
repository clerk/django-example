from clerk_backend_api import authenticate_request, AuthenticateRequestOptions
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework.exceptions import NotAuthenticated

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
            request_state = authenticate_request(
                request,
                AuthenticateRequestOptions(
                    secret_key=settings.CLERK_API_SECRET_KEY,
                    authorized_parties=settings.CLERK_AUTHORIZED_PARTIES,
                ),
            )
            if request_state.reason:
                return None
        except Exception:
            raise NotAuthenticated('Invalid token')

        # Ideally at this point user object must be fetched from DB and returned, but we will just return a dummy
        # user object
        user = User(username=request_state.payload["sub"], password="None")
        return user, None

    def authenticate_header(self, request):
        # By default, if Authorization header is present Django maps the exception to 403 Forbidden This method makes
        # DRF return 401 with WWW-Authenticate header, This is optional though if you are okay with 403
        return 'Bearer realm="api"'
