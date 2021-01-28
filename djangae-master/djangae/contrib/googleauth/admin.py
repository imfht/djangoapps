

from django.contrib import admin

from .models import (
    Group,
    User,
    UserPermission,
)

admin.site.register(User)
admin.site.register(Group)
admin.site.register(UserPermission)
