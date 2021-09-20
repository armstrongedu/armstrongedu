# from rest_framework import permissions
#
#
# class EmailPermission(permissions.BasePermission):
#     message = 'Confirm Email first.'
#
#     def has_permission(self, request, view):
#         return request.user.is_confirmed
#
#
# class UserPermission(permissions.BasePermission):
#     message = 'Not User.'
#
#     def has_object_permission(self, request, view, obj):
#         return request.user.id == obj.id
