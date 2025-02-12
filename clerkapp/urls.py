from django.urls import path

from .views import clerk_jwt, get_gated_data

urlpatterns = [
    path('clerk_jwt/', clerk_jwt),
    path('gated_data/', get_gated_data),
]
