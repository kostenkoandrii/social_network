from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):

	def has_object_permission(self, request, view, obj):
		return obj.author == request.user


class IsUserOwner(BasePermission):

	def has_object_permission(self, request, view, obj):
		return obj.id == request.user.id
