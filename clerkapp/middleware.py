from django.conf import settings
from clerk_backend_api.jwks_helpers import (
    AuthenticateRequestOptions,
    authenticate_request,
    AuthStatus,
)


class ClerkAuthMiddleware:
    """
    Middleware that adds a `verified_clerk_token` attribute to request objects
    before the view is called, which is `None` if the token verification failed,
    or the decoded access token if it succeeded.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_state = authenticate_request(
            request,
            AuthenticateRequestOptions(
                secret_key=settings.CLERK_SECRET_KEY,
                authorized_parties=settings.CLERK_AUTHORIZED_PARTIES,
            ),
        )

        if request_state.status != AuthStatus.SIGNED_IN:
            request.verified_clerk_token = None
        else:
            request.verified_clerk_token = request_state.payload

        response = self.get_response(request)

        return response
