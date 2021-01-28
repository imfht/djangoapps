from django.urls import path

from . import views

urlpatterns = [
    path('start', views.start, name="instance_start"),
    path('stop', views.stop, name="instance_stop"),
    path('warmup', views.warmup, name="instance_warmup"),
    path('clearsessions', views.clearsessions, name="clearsessions"),
]
