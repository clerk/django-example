from functools import wraps

from clerk_backend_api import authenticate_request, AuthenticateRequestOptions
from django.contrib.auth import authenticate
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.http import JsonResponse

from clerkproject import settings


class JwtAuthBackend(BaseBackend):
    def authenticate(self, request, **kwargs):
        if 'Authorization' not in request.headers:
            return None

        try:
            request_state = authenticate_request(
                request,
                AuthenticateRequestOptions(
                    secret_key=settings.CLERK_API_SECRET_KEY,
                    authorized_parties=settings.CLERK_AUTHORIZED_PARTIES,
                ),
            )
            if not request_state.is_signed_in:
                request.error_message = request_state.message
                return None
            # Ideally at this point user object must be fetched from DB and returned, but we will just return a dummy
            # user object
            user = User(username=request_state.payload["sub"], password="None")
            return user

        except Exception as e:
            request.error_message = "Unable to authenticate user"
            return None

    def get_user(self, user_id):
        return User(username=user_id, password="None")


def jwt_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = authenticate(request)
        if not user:
            error = getattr(request, 'error_message', 'User not authenticated')
            return JsonResponse({'detail': error}, status=401)
        request.user = user
        return view_func(request, *args, **kwargs)

    return _wrapped_view
