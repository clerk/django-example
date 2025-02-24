from django.http import JsonResponse, HttpResponse


def clerk_jwt(request):
    if request.verified_clerk_token is None:
        return JsonResponse({"userId": None})
    return JsonResponse({"userId": request.verified_clerk_token["sub"]})


gated_data = {"foo": "bar"}


def get_gated_data(request):
    if request.verified_clerk_token is None:
        return HttpResponse("Unauthorized", status=401)
    return JsonResponse(gated_data)
