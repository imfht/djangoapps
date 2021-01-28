"""
    This is duplicated from Django 3.0 to avoid
    starting an import chain that ends up with
    ContentTypes which may not be installed in a
    Djangae project.
"""


class BaseBackend:
    def authenticate(self, request, **kwargs):
        return None

    @classmethod
    def can_authenticate(cls, request):
        """
            This is a pre-check to see if the credentials are
            available to try to authenticate.
        """
        return True

    def get_user(self, user_id):
        return None

    def get_user_permissions(self, user_obj, obj=None):
        return set()

    def get_group_permissions(self, user_obj, obj=None):
        return set()

    def get_all_permissions(self, user_obj, obj=None):
        return {
            *self.get_user_permissions(user_obj, obj=obj),
            *self.get_group_permissions(user_obj, obj=obj),
        }

    def has_perm(self, user_obj, perm, obj=None):
        return perm in self.get_all_permissions(user_obj, obj=obj)
