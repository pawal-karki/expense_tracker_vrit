from rest_framework import permissions


class IsOwnerOrSuperuser(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Superusers can access all objects.
    """

    def has_object_permission(self, request, view, obj):
        # if the user is superadmin then they can access all objects
        if request.user.is_superuser:
            return True
        
        # only the regular  users can access their own objects
        return obj.user == request.user 