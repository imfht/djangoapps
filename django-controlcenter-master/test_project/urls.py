from django.contrib import admin

try:
    from django.urls import path
except ImportError:
    from django.conf.urls import url as path

from controlcenter.views import controlcenter


urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/dashboard/', controlcenter.urls),
]
