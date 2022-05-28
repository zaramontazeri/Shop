
from django.contrib.auth import get_user_model
from drf_extra_fields.relations import PresentablePrimaryKeyRelatedField
from media_app.serializers import ImageRelatedField, ImageSmallSerializer
from shop.serializers import  ProductDetailSerializer,\
   WorkingTimeSerilizer
from shop.models import  Menuitem, Product, ProductAttribute, ProductGalleryImage, ProductVariation, ProductVariationAttribute, Shop

from django.db.models import Value
from django.db.models.functions import Coalesce, Least
from django.utils.datetime_safe import date, datetime
from rest_framework import serializers
from rest_framework.exceptions import MethodNotAllowed, ParseError, NotFound
from drf_writable_nested.serializers import WritableNestedModelSerializer

from drf_writable_nested.serializers import WritableNestedModelSerializer
from drf_writable_nested.mixins import UniqueFieldsMixin

User = get_user_model()

class MenuitemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menuitem
        fields = '__all__'
        ref_name  = "panel_menuitem"
class ProductGalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductGalleryImage
        exclude=["product"]
        ref_name  = "panel_productgalleryimage"


class ProductSerializer(WritableNestedModelSerializer):
    menuitem = PresentablePrimaryKeyRelatedField(
        queryset=Menuitem.objects.all(),
        presentation_serializer=MenuitemSerializer,
        read_source=None,
    )
    product_images = ProductGalleryImageSerializer(many=True)
    class Meta:
        model=Product
        exclude=["related_products"]

class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductAttribute
        fields = ["id","title",]
        ref_name  = "panel_productattribute"

class ProductVariationAttributeSerializer(serializers.ModelSerializer):
    attribute = PresentablePrimaryKeyRelatedField(
        queryset=ProductAttribute.objects.all(),
        presentation_serializer=ProductAttributeSerializer,
        read_source=None,
    )
    class Meta:
        model=ProductVariationAttribute
        fields=['id','attribute','attribute_value'] #'attribute','attribute_value'
        ref_name  = "panel_productvariationattribute"

class VariationAdminSerializer(WritableNestedModelSerializer):
    specifications=ProductVariationAttributeSerializer(source='productvariationattribute_set', many=True)
    product = PresentablePrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        presentation_serializer=ProductSerializer,
        read_source=None,
    )
    # cover = ImageRelatedField()
    occasional_discount=serializers.StringRelatedField()
    class Meta:
        model = ProductVariation
        fields =["id","title_size","price","discount_price","occasional_discount","specifications","created_at","updated_at",'product']