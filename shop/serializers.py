import decimal

from django.db.models import Value
from django.db.models.functions import Coalesce, Least
from django.utils.datetime_safe import date, datetime
from rest_framework import serializers
from rest_framework.exceptions import MethodNotAllowed, ParseError, NotFound
from shop.models import Shop, Product, Menuitem, ProductVariation, ProductVariationAttribute, ProductAttribute, \
    ProductGalleryImage, ProductReview, DiscountCode, PromotionalCode,WorkingTime,OrderedItem,Transactions,Invoice,Seller
from drf_writable_nested import WritableNestedModelSerializer

class WorkingTimeSerilizer(serializers.ModelSerializer):
    day_of_week = serializers.SerializerMethodField()
    class Meta:
        model= WorkingTime
        fields = '__all__'
    def get_day_of_week (self,instance):
        days = {
            "1":"شنبه",
            "2":"یک شنبه",
            "3":"دو شنبه",
            "4":"سه شنبه",
            "5":"چهارشنبه",
            "6":"پنج شنبه",
            "7":"جمعه"
        }
        return days[instance.day]


###PRODUCT LIST
##############MANY2MANY WITH THROUGH  NESTED SERIALIZER#################################################
# class ProductAttributeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=ProductAttribute
#         fields =['title']

class ProductVariationAttributeSerializer(serializers.ModelSerializer):
    attribute = serializers.StringRelatedField()# I USED DED STR IN MODEL THAT SHOWS TITLE
    class Meta:
        model=ProductVariationAttribute
        fields=['id','attribute','attribute_value'] #'attribute','attribute_value'
        ref_name  = "app_productvariationattribute"

class VariationPriceSerializer(serializers.ModelSerializer):
    # specifications=ProductAttributeSerializer(many=True,read_only=True)
    specifications=ProductVariationAttributeSerializer(source='productvariationattribute_set', many=True)
    #IT IS IMPORTANT TO USE RELATED_NAME in models AND SOURCE in serializer . beCuz Calling the serializer for a ManyToManyField only works on the end point (i.e. ProductAttribute in this case).
    #link: 1-problem:https://www.reddit.com/r/django/comments/6yrh9k/drf_serialization_not_working_on_many_to_many/
    #link: solution:https://www.reddit.com/r/django/comments/6yrh9k/drf_serialization_not_working_on_many_to_many/dms01dv/
    occasional_discount=serializers.StringRelatedField()
    # discount_price=serializers.ReadOnlyField()
    class Meta:
        model = ProductVariation
        fields =["id","title_size","price","discount_price","occasional_discount","specifications","created_at","updated_at"]



class ProductListSerializer(serializers.ModelSerializer):
    #todo u need to add star rating later
    variations = serializers.SerializerMethodField()

    class Meta:
        model=Product
        fields = ['id','cover','title','variations']
        read_only_fields=["id"]
    def get_variations(self,instance):
        # today = date.today()
        # today_str = datetime.today().strftime("%A")
        # Query = Q(variations__special_dates__start_date__gte=today) | Q(
        #     variations__special_dates__end_date__gte=today) | Q(variations__special_dates__day=today_str.lower())
        variations = instance.variations.all().annotate(final_price=Least("price",Coalesce("discount_price", Value(100000000000)))).order_by("final_price")

        # for variation in variations.all():
        #     print(variation.final_price)
        #variations = instance.variations.all()

        return VariationPriceSerializer(variations,many=True).data

################### PRODUCT DETAIL####################
class ProductGalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductGalleryImage
        exclude=["product"]
        ref_name ="app_productgalleryimage"

class RelatedProductSerializer(serializers.ModelSerializer):
    variations_best_price=serializers.SerializerMethodField()
    class Meta:
        model=Product
        fields = ['id','cover','title','variations_best_price']

    def get_variations_best_price(self,instance):
        variations = instance.variations.all().annotate(
            final_price=Least("price", Coalesce("discount_price", Value(100000000000)))).order_by("final_price")
        best_price = variations[0].final_price
        return str(best_price)


class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductReview
        exclude=["product"]

class ProductDetailSerializer(serializers.ModelSerializer):
    product_images=ProductGalleryImageSerializer(many=True) #if I wanted to use other name I had to use source=product_images
    variations=VariationPriceSerializer(many=True)
    related_products=RelatedProductSerializer(many=True)
    product_reviews=serializers.SerializerMethodField()
    class Meta:
        model=Product
        fields="__all__"
    def get_product_reviews(self,instance):
        # query=ProductReview.objects.filter(product=instance,confirmed=True) this is equal to next line
        query_set= instance.product_reviews.filter(confirmed=True)
        return ProductReviewSerializer(query_set, many=True).data


class MenuitemSerializer(serializers.ModelSerializer):
    products = ProductDetailSerializer(many=True)
    class Meta:
        model = Menuitem
        exclude = ['shop']
        ref_name  = "app_menuitem"

class ShopSerializer(WritableNestedModelSerializer):
    working_times=WorkingTimeSerilizer(many=True)
    menu_items = MenuitemSerializer(many=True)
    class Meta:
        model= Shop
        fields = '__all__'
        read_only_fields = ["menu_itmes"]

class DiscountCodeSerializer(serializers.ModelSerializer):
    final_price = serializers.SerializerMethodField()
    class Meta:
        model = DiscountCode
        fields = [
            # 'is_used',
            'code',
            'percentage',
            'maximum_value',
            'expire_at',
            # 'inventory',
            "final_price"
        ]
    def get_final_price(self, obj):
        # var_id = self.context.get("var_id")
        ## number_of_people = self.context.get("number_of_people")

        basket = self.context.get("basket")

        today = date.today()
        discount = 0
        max_discount_value = 0
        if  today < obj.expire_at: # and obj.inventory>0
            discount = obj.percentage
            max_discount_value = obj.maximum_value
        else :
            raise ParseError(detail={"error": "discount is expired", "error_code": "4006"})


        #change to for loop
        populate_items_price=0
        for item in basket:
            try:
                variation_object = ProductVariation.objects.get(id=item["var_id"])
                effective_price = variation_object.discount_price if variation_object.discount_price else variation_object.price
                populate_items_price+= (item["qty"] * float(effective_price)) #todo check for outcome
            except:
                ParseError(detail={"error": "product not found", "error_code": "4007"})


        # var = ProductVariation.objects.get(id=var_id)
        # effective_price = var.discount_price if var.discount_price else var.base_price
        # p = number_of_people *float(effective_price) #populate_items_price hamoon p hast
        #

        #TODO : HATMAN BA ELNAZ MATRAH KON
        if discount != 0:
            # max_discount_value = convert(currency, max_discount_value)
            if (float(populate_items_price) < float(max_discount_value) or  max_discount_value ==0):
                final_price =round( (float(populate_items_price) - (float(populate_items_price) * float(discount) / 100.0)))
            else:
                final_price = round(float(populate_items_price) - (float(max_discount_value) * float(discount) / 100.0))
        else :
            raise ParseError(detail={"error": "discount is zero", "error_code": "4007"})
        return decimal.Decimal("{:.2f}".format(final_price))



class PromotionalCodeSerializer(serializers.ModelSerializer):
    var_price = serializers.SerializerMethodField()
    class Meta:
        model = PromotionalCode
        fields = '__all__'

    def get_var_price(self, obj):
        request = self.context.get("request")
        basket = self.context.get("basket")

        today = date.today()
        discount = 0
        max_discount_value = 0
        if bool(request.user and request.user.is_authenticated):
            if  today < obj.expire_at: #todo inventory? (obj.inventory > 0 and) come back and discuss it after INVOICE
                discount = obj.percentage
                max_discount_value = obj.maximum_value
            else:
                raise ParseError(detail={"error": "discount is expired", "error_code": "4006"})

        populate_items_price=0
        for item in basket:
            try:
                variation_object = ProductVariation.objects.get(id=item["var_id"])
                effective_price = variation_object.discount_price if variation_object.discount_price else variation_object.price
                populate_items_price+= item["qty"] * float(effective_price) #todo check for outcome
            except:
                ParseError(detail={"error": "product not found", "error_code": "4007"})


        if discount != 0:
            if (float(populate_items_price) < float(max_discount_value)):
                tour_price =round (float(populate_items_price) - (float(populate_items_price) * float(discount) / 100.0))
            else:
                tour_price =round(float(populate_items_price) - (float(max_discount_value) * float(discount) / 100.0))
        else:
            raise ParseError(detail={"error": "discount is zero", "error_code": "4001"})
        return decimal.Decimal("{:.2f}".format(tour_price))


# todo : variation ha ham agar to invoice ii boodan shadow delete eshoon kon
class OrderedItemSerializer(serializers.ModelSerializer):
    # product_item_info = serializers.SerializerMethodField() #variation
    # I get the name of the product variation here
    # product_variation_item = serializers.StringRelatedField()

    class Meta:
        model = OrderedItem
        # IMP: I  use unit price so your previous invoices won't be incorrect after you changed a food's price.
        fields = (
            'pk',
            'product_variation_item',
            'qty',
            'unit_base_price',  # todo  tooye save hatman ino az variation begir
            'unit_discount_price',  # todo  tooye save hatman ino az variation begir
            # 'invoice' #????????
        )
        read_only_fields = ('pk', 'unit_base_price', 'unit_discount_price')

# class TourPaymentSerializer(serializers.ModelSerializer):



class InvoiceSerializer(serializers.ModelSerializer):
    orders = OrderedItemSerializer(many=True)
    # customer_info = serializers.SerializerMethodField()
    class Meta:
        model = Invoice

        fields = (
            'pk',
            'shipping_number',  # todo ????
            'order_status',
            'deliver_status',
            'delivery_type',
            'customer',
            'orders',
            # todo??????benazaram bejash code ro to view begir inja bezaresh tooye gheymat?
            'discount_code',
            'total_price',
            'date',
            'address',
            'description',
            'shop',
            'seller'
            # 'transaction'
        )
        read_only_fields = ('order_status','deliver_status','discount_code','total_price',"date",'customer','shop') #todo?

    # def get_customer_info(self,obj):
    #     customer_id=obj.customer
    #     customer_serializer = CustomerSerializer(obj.customer)
    #     res = customer_serializer.data
    #     return res

    def create(self, validated_data):
        basket = validated_data.pop('orders')
        try:
            address = validated_data.pop("address")
        except:
            pass #please add address
        order_status = "draft"

        total_price = 0
        today = date.today()
        discount = self.context["discount"]
        max_discount_value = 0
        if discount:
            if today < discount.expire_at:  # and obj.inventory>0
                discount = discount.percentage
                max_discount_value = discount.maximum_value
            else:
                raise ParseError(
                    detail={"error": "discount is expired", "error_code": "4006"})
        else:
            discount = 0
        # change to for loop
        populate_items_price = 0
        for item in basket:
            try:
                # variation_object = ProductVariation.objects.get(
                #     id=item["var_id"])
                effective_price = dict(item)['product_variation_item'].discount_price if dict(item)['product_variation_item'].price   else  dict(item)['product_variation_item'].discount_price 
                # todo check for outcome
                populate_items_price += (dict(item)["qty"] * float(effective_price))
            except:
                ParseError(
                    detail={"error": "product not found", "error_code": "4007"})

        # var = ProductVariation.objects.get(id=var_id)
        # effective_price = var.discount_price if var.discount_price else var.base_price
        # p = number_of_people *float(effective_price) #populate_items_price hamoon p hast
        #

        # TODO : HATMAN BA ELNAZ MATRAH KON
        final_price = populate_items_price
        if discount != 0:
            # max_discount_value = convert(currency, max_discount_value)
            if (float(populate_items_price) < float(max_discount_value) or max_discount_value == 0):
                final_price = round((float(
                    populate_items_price) - (float(populate_items_price) * float(discount) / 100.0)))
            else:
                final_price = round(float(
                    populate_items_price) - (float(max_discount_value) * float(discount) / 100.0))
        # else:
        #     raise ParseError(
        #         detail={"error": "discount is zero", "error_code": "4007"})
        # set config vat 
        vat = 0
        vtax = round(float(vat) * float(final_price) / 100.0)
        final_price = round(float(
                    populate_items_price) + (float(vat) * float(final_price) / 100.0))
        #shipping value 
        shipping_price = 0
        final_price = shipping_price +final_price
        final_price = decimal.Decimal("{:.2f}".format(final_price))

        seller = Seller.objects.first(shop= self.context["shop"])

        invoice = Invoice(**validated_data)
        invoice.total_price = final_price
        invoice.customer = self.context["request"].user
        invoice.deliver_status = "pe"
        invoice.order_status = "dr"
        invoice.address = address
        invoice.shipping_price = shipping_price
        invoice.vtax = vtax 
        invoice.seller = seller
        if self.context["discount_type"] == "discount":
            invoice.discount_code = discount
        elif  self.context["discount_type"] == "promotional":
            invoice.promotional_code = discount
        


        invoice.save()
        return invoice


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transactions
        fields = (
            'pk',
            # 'invoice', #???
            'refId',
            'bankRefId',
            'status',
            # 'statusNum' ???
            'authority'
        )
