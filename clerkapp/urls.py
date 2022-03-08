from django.urls import path

from .views import clerk_jwt

urlpatterns = [
    path('clerk_jwt/', clerk_jwt),
]