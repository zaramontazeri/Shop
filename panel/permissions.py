from rest_framework import permissions
from shop import models

class IsShopUserOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        sellers = models.Seller.objects.filter(seller= request.user)
        shops= [seller.shop.id for seller in sellers]

        return obj.shop.id in shops or request.user.is_superuser