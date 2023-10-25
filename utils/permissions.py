from rest_framework import permissions

from account.apps import AccountConfig as UserConf


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.user_type == UserConf.USER_ADMIN)


class IsInvestor(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.user_type == UserConf.USER_INVESTOR)


class IsSponsor(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.user_type == UserConf.USER_SPONSOR)


def IsSuperAdmin(request):
    return bool(
        request.user and (
            request.user.user_type == UserConf.USER_ADMIN or
            'admin' in request.user.email
        )
    )
