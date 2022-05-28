from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (ShopListAPIView,
                    ShopAPIView,
                    ProductsListAPIView,
                    MenuItemListAPIView,
                    ProductsShopListAPIView,
                    ProductDetailView,
                    InvoiceView,
                    DiscountCheck)
# OrderedItemViewSet

# router = DefaultRouter()
# router.register(r'ordereditem', OrderedItemViewSet)
# urlpatterns = router.urls
# urlpatterns = +[
urlpatterns = [
    path('shops/', ShopListAPIView.as_view()),
    path('shop/<int:pk>/', ShopAPIView.as_view()),
    path('products/<int:c_id>/', ProductsShopListAPIView.as_view(), name='products_category'),
    path('products/', ProductsListAPIView.as_view(), name='products'),
    path('product_detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path("discount_check/", DiscountCheck.as_view(),name="discount_check"),
    path('invoice/', InvoiceView.as_view(), name='products'),
    path('menu_items/<int:c_id>/', MenuItemListAPIView.as_view(), name='subcategories'),
]
