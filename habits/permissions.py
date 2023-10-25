from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """ Custom permission class to check if a user is the owner of an object. """

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner