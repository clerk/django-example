from django.urls import path

from .views import clerk_jwt, gated_data

urlpatterns = [
    path('clerk_jwt/', clerk_jwt),
    path('gated_data/', gated_data),
]