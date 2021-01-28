

from django.urls import path
from .handlers import deferred_handler

urlpatterns = [
    path('deferred/', deferred_handler, name="tasks_deferred_handler")
]
