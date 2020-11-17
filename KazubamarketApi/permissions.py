from rest_framework import permissions

########## Admin User's Permissions ##########
class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.admin)

########## Activated User's Permissions ##########
class IsActivatedUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.referral.has_paid_activation)

########## Subscribed User's Permissions ##########
class IsSubscribedUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_subscribe)

########## User's Owner Permissions ##########
class UserIsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id