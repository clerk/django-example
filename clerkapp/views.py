from django.http import JsonResponse

from clerkapp.auth import jwt_required


@jwt_required
def clerk_jwt(request):
    data = {
        'userId': request.user.username,
    }
    return JsonResponse(data)


@jwt_required
def gated_data(request):
    data = {
        "foo": "bar",
    }
    return JsonResponse(data)
