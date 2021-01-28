# THIRD PARTY
from django.urls import path

# DJANGAE
from .views import cleanup_locks


urlpatterns = [
    path('djangae-cleanup-locks/', cleanup_locks, name="cleanup_locks"),
]
