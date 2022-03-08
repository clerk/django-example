from django.shortcuts import render
from django.http import JsonResponse
from jose import jwt

from urllib.request import urlopen
import json

def clerk_jwt(request):
    # Strip the "Bearer " prefix from the header
    token = request.headers['Authorization'][7:]

    # Update this to 'https://{clerk_frontend_api}/.well-known/jwks.json'
    # Note: The content of this endpoint will never change, so it should
    # be cached on the server instead of requested with each API call
    url = 'https://clerk.clerk.dev/.well-known/jwks.json'
    response = urlopen(url)
    data_json = json.loads(response.read())

    decoded = jwt.decode(token, data_json['keys'][0], algorithms=['RS256'])

    data = {
        'userId': decoded['sub'],
    }
    return JsonResponse(data)