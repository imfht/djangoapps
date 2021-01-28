from django.urls import path

from . import views

urlpatterns = (
    path(
        'create-datastore-backup/',
        views.create_datastore_backup,
        name="create_datastore_backup"
    ),
)
