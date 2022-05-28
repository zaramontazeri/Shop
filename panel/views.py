from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from shop import models
from shop import serializers
from panel import serializers as admin_serializers

from shop.models import Invoice, ProductVariation
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response
from shop.serializers import InvoiceSerializer
from django.shortcuts import render

# Create your views here.

class OrdersListAPIView(ListAPIView):
    ''' 
        
    '''
    serializer_class = InvoiceSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(Invoice.objects.filter(shop=kwargs.get("shop"),deliver_status=kwargs.get("status")))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ChangeOrderDeliverStatus(UpdateAPIView):
    permission_classes=(IsAuthenticated,)
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        deliver_status = request.data.get('deliver_status',None)
        if deliver_status :
            invoice = Invoice.objects.get(pk=kwargs.get("pk"))
            invoice.deliver_status=deliver_status
            invoice.save()
        else :
            return Response({"status":"not_changed"})
        return Response({"status":deliver_status})


class ProductsViewSet(viewsets.ModelViewSet):
    """ViewSet for the OrderItem class"""
    queryset = models.Product.objects.all()
    serializer_class = admin_serializers.ProductSerializer
    def list(self,request):
        queryset = models.Product.objects.all()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializers.ProductDetailSerializer(page, many=True,context={"request":request})
            return self.get_paginated_response(serializer.data)

        serializer = serializers.ProductDetailSerializer(queryset, many=True,context={"request":request})
        return Response(serializer.data)


class ProductVariationViewSet(viewsets.ModelViewSet):
    """ViewSet for the ProductVariations class"""
    queryset = models.ProductVariation.objects.all()
    serializer_class = admin_serializers.VariationAdminSerializer

class ProductVarEnable(UpdateAPIView):
    permission_classes=(IsAuthenticated,)
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        enable = request.data.get('enable',None)
        if enable :
            variation = ProductVariation.objects.get(pk=kwargs.get("pk"))
            variation.enable=enable
            variation.save()
        else :
            return Response({"status":"not_changed"})
        return Response({"status":enable})

class ShopViewSet(viewsets.ModelViewSet):
    """ViewSet for the Shop class"""
    queryset = models.Shop.objects.all()
    serializer_class = serializers.ShopSerializer

class ProductAttributeViewSet(viewsets.ModelViewSet):
    """ViewSet for the OrderItem class"""
    queryset = models.ProductAttribute.objects.all()
    serializer_class = admin_serializers.ProductAttributeSerializer

class MenuItemViewSet(viewsets.ModelViewSet):
    """ViewSet for the OrderItem class"""
    queryset = models.Menuitem.objects.all()
    serializer_class = admin_serializers.MenuitemSerializer



# class ShopUserListView(ListAPIView):
#     serializer_class = UserSerializer
#     def get_queryset(self):
#         group = Group.objects.get(name='shop_manager') 
#         self.queryset = User.objects.filter(groups=group)
#         return super().get_queryset()

# class ShopUserCreateView(CreateAPIView):
#     serializer_class = AdminUserCreateSerializer
#     def create(self, request, *args, **kwargs):
#         addresses = request.data.pop("addresses",None)
#         data=request.data
#         serializer = self.get_serializer(data=data)
#         serializer.is_valid(raise_exception=True)
#         user = self.perform_create(serializer)
#         group = Group.objects.get(name='shop_manager') 
#         group.user_set.add(user)
#         if addresses is not None:
#             for address in addresses:
#                 address["user"]=user.id
#                 address_serializer = AddressSerializer(data=address)
#                 if address_serializer.is_valid(raise_exception=True):
#                     address_serializer.save()

#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#     def perform_create(self, serializer):
#         return serializer.save()

# class ShopUserRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
#     serializer_class = UserAddressSerializer
#     # def 
#     def get_queryset(self):
#         group = Group.objects.get(name='shop_manager') 
#         self.queryset = User.objects.filter(groups=group)    
#         return super().get_queryset()

#     def get_serializer_context(self):
#         return   {
#             'request': self.request,
#             'format': self.format_kwarg,
#             'view': self,
#             'user_id':self.kwargs["pk"]
#         }
#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         data =request.data

#         for address in data['addresses']:
#             address.update({"user":kwargs["pk"]})
#         serializer = self.get_serializer(instance, data=data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#         if getattr(instance, '_prefetched_objects_cache', None):
#             # If 'prefetch_related' has been applied to a queryset, we need to
#             # forcibly invalidate the prefetch cache on the instance.
#             instance._prefetched_objects_cache = {}
#         return Response(serializer.data)
        
