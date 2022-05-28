from django.conf.urls import url
from rest_framework_simplejwt import views
from auth_rest_phone.jwt.views import CustomTokenObtainPairView, CustomTokenShopObtainPairView,Login,RefreshToken,Logout,CustomTokenOtpObtainPairView
from django.urls import path


urlpatterns = [
    url(r"^jwt/create/?", CustomTokenObtainPairView.as_view(), name="jwt-create"),
    # url(r"^jwt/create/?", views.TokenObtainPairView.as_view(), name="jwt-create"),
    url(r"^jwt/refresh/?", views.TokenRefreshView.as_view(), name="jwt-refresh"),
    url(r"^jwt/verify/?", views.TokenVerifyView.as_view(), name="jwt-verify"),
    url(r"^jwt/otp/?", CustomTokenOtpObtainPairView.as_view(), name="jwt-otp-create"),
    url(r"^jwt/shop/?", CustomTokenShopObtainPairView.as_view(), name="jwt-shop-create"),

    # path("jwt_c/create/", Login.as_view(), name="jwt_c-create"),
    # path("jwt_c/refresh/", RefreshToken.as_view(),name="jwt_c-refresh"),
    # path("jwt_c/logout/", Logout.as_view(), name="jwt_c-logout"),

]
