from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (ChangeOrderDeliverStatus, MenuItemViewSet, OrdersListAPIView, ProductAttributeViewSet, ProductVarEnable, ProductVariationViewSet, ProductsViewSet, ShopViewSet)

router = DefaultRouter()
router.register(r'shop', ShopViewSet)
router.register(r'product', ProductsViewSet)
router.register(r'variation', ProductVariationViewSet)
router.register(r'attribute', ProductAttributeViewSet)
router.register(r'menuitem', MenuItemViewSet)
urlpatterns = router.urls
urlpatterns += [    
    path('change_status_order/<int:pk>/', ChangeOrderDeliverStatus.as_view()),
    path('orders/<int:shop>/<str:status>/', OrdersListAPIView.as_view()),
    path('productvar_enable/<int:pk>/', ProductVarEnable.as_view()),
]
