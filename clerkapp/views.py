from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes

from clerkapp.auth import JwtAuthentication


# We are using @authentication_classes([JwtAuthentication]) decorator to apply the authentication class to the view
# this can also be applied globally in settings.py using DEFAULT_AUTHENTICATION_CLASSES, see example:
# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'clerkapp.auth.JwtAuthentication',
#     ),
# }

@api_view(['GET'])
@authentication_classes([JwtAuthentication])
def clerk_jwt(request):
    data = {
        'userId': request.user.username,
    }
    return JsonResponse(data)


@api_view(['GET'])
@authentication_classes([JwtAuthentication])
def gated_data(request):
    data = {
        'foo': 'bar',
    }
    return JsonResponse(data)
