"""chita_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from drf_yasg2 import openapi
from drf_yasg2.views import get_schema_view
from coooli_backend import settings
from rest_framework import permissions
from django.views.static import serve
from django.urls import path, include
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)  # https://drf-yasg.readthedocs.io/en/stable/rendering.html
# https://drf-yasg.readthedocs.io/en/stable/readme.html#installation

urlpatterns = [
    url(r'^docs(?P<format>\.json|\.yaml)$', schema_view.without_ui(
        cache_timeout=0), name='schema-json'),
    url(r'^docs/$', schema_view.with_ui('swagger',
                                        cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc',
                                         cache_timeout=0), name='schema-redoc'),
    path('api-auth/', include('rest_framework.urls')),
    # path('api/auth', include('auth_rest.urls')),
    # path('api/auth', include('auth_rest.urls.jwt')),
    # path('api/auth/', include('auth_rest.social.urls')),
    path('api/auth/', include('auth_rest_phone.urls')),
    path('api/auth/', include('auth_rest_phone.urls.jwt')),
    path('admin/', admin.site.urls),
    path('api/shop/', include('shop.urls')),
    path('api/panel/', include('panel.urls')),
    path('api/media_app/', include('media_app.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
