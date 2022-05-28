
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.fields import related
from django.utils.html import format_html
from django.conf import settings
from decimal import Decimal
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import ArrayField
from media_app import models as media_models
class ShopCategory(models.Model):
    # Fields
    name = models.CharField(max_length=255)
    # slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s' % self.slug

    # def get_absolute_url(self):
    #     return reverse('supplier_suppliercategory_detail', args=(self.slug,))


    # def get_update_url(self):
    #     return reverse('supplier_suppliercategory_update', args=(self.slug,))

class ShopSubCategory(models.Model):
    # Fields
    name = models.CharField(max_length=255)
    # slug = extension_fields.AutoSlugField(populate_from='name', blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    # Relationship Fields
    category = models.ForeignKey(
        'shop.ShopCategory',
        on_delete=models.CASCADE, related_name="suppliers", 
    )

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s-%s' % self.slug,self.category.slug

    # def get_absolute_url(self):
    #     return reverse('supplier_suppliercategory_detail', args=(self.slug,))


    # def get_update_url(self):
    #     return reverse('supplier_suppliercategory_update', args=(self.slug,))

class Shop(models.Model):
    title = models.CharField(max_length=64)
    slug = models.SlugField(allow_unicode=True)
    cover = models.ForeignKey(media_models.Image , on_delete=models.SET_NULL,null=True,blank=True,related_name="shops")
    header = models.ForeignKey(media_models.Image , on_delete=models.SET_NULL,null=True,blank=True)
    phone_numbers = ArrayField(models.CharField(verbose_name=_("phone number"),max_length=20,blank=True))
    full_address=models.TextField(verbose_name=_("full address"))
    description=models.TextField(verbose_name=_("description"),null=True,blank=True)
    order = models.IntegerField(verbose_name=_("order"),unique=True)
    enable = models.BooleanField(verbose_name=_("enable"),default=True)
    # Relationship Fields
    subcategory = models.ForeignKey(
        'shop.ShopSubCategory',
        on_delete=models.CASCADE, related_name="suppliers", 
    )

    class Meta:
        ordering = ('-order',)
        verbose_name = _('Restaurant Branch')
        verbose_name_plural = _('Restaurant Branchs')

    def __str__(self):
        return  self.title

    # def get_absolute_url(self):
    #     return reverse('burger:burger_menu', args=(self.pk,))


    # def get_update_url(self):
    #     return reverse('burger_restaurantbranch_update', args=(self.pk,))

    class Meta:
        verbose_name = 'Shop '
        verbose_name_plural = 'Shop Categories'

    def __str__(self):
        return self.title

class Seller(models.Model):
    seller = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL)
    shop = models.ForeignKey(Shop,null=True,blank=True,on_delete=models.SET_NULL)

class Menuitem(models.Model):
    title = models.CharField(max_length=64)
    slug = models.SlugField(allow_unicode=True)
    shop=models.ForeignKey(Shop,related_name="menu_items",on_delete=models.PROTECT)
    def __str__(self):
        return self.shop.title+"__"+self.title

# class MenuitemSpecifications(models.Model):
#     specification_key = models.CharField(max_length=128)
#     specification_value = models.CharField(max_length=128)
#     promotional_gift=models.ForeignKey(Menuitem,related_name="specifications",on_delete=models.CASCADE)
#     class Meta(object):
#         ordering = ['specification_key']
#
#     def __str__(self):
#         return self.specification_key


class Product(models.Model):
    #todo rating
    cover = models.ForeignKey(media_models.Image , on_delete=models.SET_NULL,null=True,blank=True,related_name="products")
    title=models.CharField(max_length=200)
    menuitem=models.ForeignKey(Menuitem,related_name="products",on_delete=models.PROTECT) #todo on_delete casacade? agar menuitem eshtebahi hazf she koli mahsool hazf mishan! che konim?
    description=models.TextField()
    related_products = models.ManyToManyField('self',blank=True,null=True, symmetrical=True)#, related_name='+' #if i used through it wasn't bi-directional and i had to do symmetrical=False
    def __str__(self):
        return self.title

class ProductGalleryImage(models.Model):
    product=models.ForeignKey(Product,related_name="product_images",on_delete=models.CASCADE)
    caption = models.CharField(max_length=128)
    image = models.ForeignKey(media_models.Image , on_delete=models.SET_NULL,null=True,blank=True,related_name="product_gallery_images")
    order = models.PositiveIntegerField(default=0, blank=False, null=False)
    def image_tag(self):
        if self.image:
            return format_html('<img src="{}" width="100" height="100" />'.format(self.image.url))
        return None
    image_tag.short_description = 'Image'

    def __str__(self):
        return self.caption

    class Meta(object):
        ordering = ['order']

class ProductAttribute(models.Model):
    title=models.CharField(max_length=150)
    def __str__(self):
        return self.title

class ProductVariation(models.Model):
    title_size=models.CharField(max_length=100)
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="variations")
    specifications = models.ManyToManyField(ProductAttribute, blank=True, through='ProductVariationAttribute',related_name='specifications_to_person')
    price = models.DecimalField(max_digits=10, decimal_places=0)
    occasional_discount= models.ForeignKey("OccasionalDiscount",related_name="occasional_discount_set",blank=True,null=True,on_delete=models.SET_NULL) #this parametere makes impact on discount price
    discount_price =models.DecimalField(max_digits=10, decimal_places=0,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    enable = models.BooleanField(default=True)
    # @property
    # def discount_price(self):
    #     discount = int(self.price)
    #     if self.occasional_discount:
    #         percentage=self.occasional_discount.percentage
    #         discount = int(float(self.price) - round((float(percentage) / 100.0) * float(self.base_price)))
    #     return discount

    def __str__(self):
        return self.product.title + " __ " +self.title_size


class ProductVariationAttribute(models.Model):
    product_variation=models.ForeignKey(ProductVariation,on_delete=models.CASCADE) #agar khode product nabashe. vojood attribute bi manie
    attribute=models.ForeignKey(ProductAttribute,on_delete=models.PROTECT) #agar attribute ro bekhaym pak konim injoori mifahmim ke oon attribute baraye baghie estefade shode
    attribute_value=models.CharField(max_length=150)

#todo rating is connected to reviews??????
class ProductReview(models.Model):
    product=models.ForeignKey(Product,related_name="product_reviews",on_delete=models.CASCADE)
    #todo USER ro moshakhas kon bepors ke daghighan modele user chejoorie ke fk be oon chejoori bashe
    user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,blank=True,on_delete=models.SET_NULL)
    comment=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rate = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
    confirmed=models.BooleanField(default=False)
    #todo write afte cheking USER: def __str__(self):
    #     return "User: {username} | Tour: {id}".format(username=self.user.username, id=self.tour.id)
    def __str__(self):
        return self.product.title +"__"+str(self.created_at.date())
class Invoice(models.Model):
    #list of status choices :paid _ unsuccessful paiment-> in transactions. deliverd
    DRAFT='dr'
    PAYED='pa'
    PENDING='pe'
    CONFIRMED='co'
    DELIVERED='de'

    SITE = 'si'
    INPLACE ='in'
    TAXI ='ta'

    ORDER_STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (PAYED,'Payed'),
    )

    DELIVER_STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
        (DELIVERED, 'Delivered'),
    )
    SELL_SOURCE = (
        (SITE, 'site'),
        (INPLACE, 'inplace'),
    )
    DELIVERY_TYPE = (
        (INPLACE,'inplace'),
        (TAXI,'taxi')
    )
    order_status=models.CharField(verbose_name=_("pay_status"),max_length=4,choices=ORDER_STATUS_CHOICES,default=DRAFT)
    deliver_status = models.CharField(verbose_name=_("deliver_status"), max_length=4, choices=DELIVER_STATUS_CHOICES, default=PENDING)
    delivery_type = models.CharField(verbose_name=_("deliver_status"), max_length=4, choices=DELIVERY_TYPE, default=TAXI)
    #TODO shange shipping_number into u_id (ask erfan)
    shipping_number=models.CharField(max_length=24,null=True,blank=True) #POSTAL TRACKING CODE
    sell_source = models.CharField(verbose_name=_("sell_source"), max_length=4, choices=SELL_SOURCE, default=SITE)
    seller = models.ForeignKey(Seller,verbose_name=_("seller"), on_delete=models.SET_NULL, null=True,blank=True) 
    shop = models.ForeignKey(Shop,verbose_name=_("shop") , on_delete=models.SET_NULL, null=True,blank=True)#from seller you can also undrestand which restaurant it is
    customer = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name=_("customer"), null=True,blank=True, on_delete=models.SET_NULL)
    # u can search usage of through in here:https://docs.djangoproject.com/en/2.2/topics/db/models/
    product_items = models.ManyToManyField(ProductVariation,verbose_name=_("product items"), through="OrderedItem")  #
    total_price=models.DecimalField(verbose_name=_("total price"),default=Decimal('0.00'),max_digits=19, decimal_places=0,null=True,blank=True)  # totalCost #todo #decimal 2 or 3?)
    #serial_number (is it secure if i use id for each invoice??? or should i make serial number myself?)
    description = models.CharField(verbose_name=_("description"),max_length=200 , null=True, blank=True)
    date = models.DateTimeField(verbose_name=_("date"),auto_now_add=True ,null=True) #todo how to make this automatic and JALALI
    # address = models.TextField(verbose_name=_("address"),null=True,default="-1")
    address = models.ForeignKey("users_info.Address",on_delete=models.PROTECT,default="-1") #if a user has address in inovice I dont let the user to delete
    #todo what about default and on_delete? talk to erfan
    discount_code = models.ForeignKey("DiscountCode" ,on_delete=models.SET("deleted"), related_name="payments", null=True) #It's first model of discounting
    promotional_code = models.ForeignKey("PromotionalCode", on_delete=models.SET("deleted"), related_name="promo_payments",null=True, blank=True) #it's user base
    shipping_price =models.DecimalField(verbose_name=_("shipping price"),default=Decimal('0.00'),max_digits=19, decimal_places=0,null=True,blank=True) 
    vtax = models.DecimalField(verbose_name=_("value added price"),default=Decimal('0.00'),max_digits=19, decimal_places=0,null=True,blank=True) 
    class Meta:
        ordering = ('-pk',)
        verbose_name = _('Invoice')
        verbose_name_plural = _('Invoices')


    def __str__(self):
        return str(self.id)+"_"+self.customer.phone

    # def get_absolute_url(self):
    #     return reverse('app_name_invoice_detail', args=(self.pk,))
    #
    #
    # def get_update_url(self):
    #     return reverse('app_name_invoice_update', args=(self.pk,))

class OrderedItem(models.Model):
    product_variation_item=models.ForeignKey(ProductVariation,verbose_name=_("product item"),null=True,blank=True, on_delete=models.SET_NULL,related_name="products") #,related_query_name="products"
    invoice=models.ForeignKey(Invoice,verbose_name=_("invoice"),on_delete=models.SET_NULL, null=True,related_name="orders")
    #todo what about on_delete???
    qty = models.IntegerField(verbose_name=_("quantity"),null=True)
    #IMP: I  use unit price so your previous invoices won't be incorrect after you changed a food's price.
    unit_base_price=models.DecimalField(verbose_name=_("unit base price"),max_digits=19, decimal_places=0) #ino az roye gheymat e product variation mirizi tooye in todo: where?
    unit_discount_price = models.DecimalField(verbose_name=_("unit discount price"),null=True,blank=True, max_digits=19, decimal_places=0)
    # todo #decimal 2 or 3?


    class Meta:
        ordering = ('-pk',)
        verbose_name = _('Ordered Item')
        verbose_name_plural = _('Ordered Items')

    def __str__(self):
        return str(self.id)+"_"+self.product_variation_item.product.title+"_"+self.product_variation_item.title_size #todo name or first+last name  +"_"+self.invoice.costumer.name

    # def get_absolute_url(self):
    #     return reverse('app_name_ordereditem_detail', args=(self.pk,))
    #
    # def get_update_url(self):
    #     return reverse('app_name_ordereditem_update', args=(self.pk,))
    #

#
# class TourPayment(models.Model):
#     created_at = models.DateTimeField(auto_now_add=True)
#     day = models.DateField()
#     paid = models.BooleanField(default=False)
#     tour_price = models.DecimalField(max_digits=12, decimal_places=2)
#
#     name = models.CharField(max_length=32)
#     email = models.EmailField()
#     phone = models.CharField(max_length=32)
#     email_notif = models.BooleanField(default=False)
#     # tour = models.ForeignKey('Tour', on_delete=models.CASCADE,
#     #                          related_name="payments")
#     user = models.ForeignKey(User, on_delete=models.SET_NULL,
#                              related_name="payments", null=True, blank=True)
#     variation = models.ForeignKey(TourVariation,related_name="payments",on_delete=models.DO_NOTHING)
#     pickup_point = models.CharField(max_length=32,null=True,blank=True) #todo
#     promotion_code = models.ForeignKey("PromotionalCode",on_delete=models.DO_NOTHING ,related_name="payments", null=True) #todo
#     discount_code = models.ForeignKey("DiscountCode" ,on_delete=models.DO_NOTHING, related_name="payments", null=True)
#     def __str__(self):
#         return str(self.id)
#



class Transactions(models.Model):
    SATAUS_CHOICES = (
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('pending',"Pending")
    )
    # amount and date #todo I have total price and date in invoice and I have a fk to invoice , should i use "amount" and "date" here too?
    invoice=models.ForeignKey(Invoice,verbose_name=_("invoice"), on_delete=models.PROTECT,related_name="transaction")
    refId = models.CharField(_("trackingCode"), max_length=100) #todo BIG_TODO what about verbose name
    bankRefId = models.CharField(verbose_name=_("bankRefId"),max_length=100)
    status = models.CharField(verbose_name=_("status"),max_length=10, choices=SATAUS_CHOICES)
    statusNum = models.IntegerField(verbose_name=_("status number"))
    # gateway = models.ForeignKey(Gateway,verbose_name=_("gateway"), on_delete=models.PROTECT)
    authority = models.CharField(verbose_name=_("authority"),max_length=20)
    class Meta:
        ordering = ('-pk',)
        verbose_name = _('Transaction')
        verbose_name_plural = _('Transactions')

    def __str__(self):
        return str(self.pk)+"_"+self.invoice.seller.branch_name.branch_name

    # def get_absolute_url(self):
    #     return reverse('app_name_transactions_detail', args=(self.pk,))
    #



class DiscountCode(models.Model): #FIRST MODEL OF DISCOUNTING we use it in invoice
    # is_used = models.BooleanField(default=False)
    code = models.CharField(max_length=64, db_index=True, unique=True, blank=True,
                            help_text='It will be fill, if you leave it empty. ex: cz6nX')
    percentage = models.SmallIntegerField(validators=(
        MinValueValidator(1), MaxValueValidator(100)))
    maximum_value = models.IntegerField(default=0) #TODO needed?
    expire_at = models.DateField()
    # inventory = models.IntegerField(default=1)
    # one_time = models.BooleanField(default=False) #todo ??????
    def __str__(self):
        return self.code


class OccasionalDiscount(models.Model): #Second way of discounting : it makes impact in product variation discount price
    title=models.CharField(max_length=200)
    # product_variation=models.ForeignKey(ProductVariation)
    percentage = models.SmallIntegerField(validators=(
        MinValueValidator(1), MaxValueValidator(100)))
    #TODO BIG todo : make sure just related items see this

    def __str__(self):
        return self.title  #+"_"+str(self.id)

class PromotionCodeStrategy(models.Model):
    # minimum_expendable_value = models.IntegerField(default=0)
    # maximum_expendable_value = models.IntegerField(default=0)
    inventory = models.IntegerField(default=0) #todo ??????????
    expire_time = models.IntegerField(default=5)
    is_for_first_order = models.BooleanField(default=False)
    percentage = models.SmallIntegerField(validators=(
        MinValueValidator(1), MaxValueValidator(100)))
    maximum_value = models.IntegerField(default=0)

class PromotionalCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=64, db_index=True, unique=True, blank=True,
                            help_text='It will be fill, if you leave it empty. ex: cz6nX')
    # inventory = models.IntegerField() #todo ??????????????
    percentage = models.SmallIntegerField(validators=(
        MinValueValidator(1), MaxValueValidator(100)))
    # minimum_expendable_value = models.IntegerField(default=0)
    maximum_value = models.IntegerField(default=0)
    num_of_used = models.IntegerField(default=0, editable=False) # ye adad bezar va har dafe tyeki azash kam kon

    expire_at = models.DateField()
    disable =  models.BooleanField(default=False)

    # strategy = models.ForeignKey(PromotionCodeStrategy,on_delete=models.DO_NOTHING,null=True)

        

class WorkingTime(models.Model):
    DATE_CHOICES = (
        ('1','shanbe'),
        ('2','yekshanbe'),
        ('3','doshanbe'),
        ('4','seshanbe'),
        ('5','charshanbe'),
        ('6','pangshanbe'),
        ('7','jome'),
    )
    day = models.CharField(verbose_name=_("day"),max_length=1,choices=DATE_CHOICES)
    from_time = models.CharField(verbose_name=_("from_times"),max_length=150)
    to_time = models.CharField(verbose_name=_("to_times"),max_length=150)
    branch = models.ForeignKey(Shop,verbose_name=_("branch"),related_name="working_times", on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Working Time')
        verbose_name_plural = _('Working Times')

    def __str__(self):
        return  str(self.branch.id)+"_"+self.day



# class Gateway(models.Model):
#     gatewayCode = models.CharField(verbose_name=_("gateway code"),max_length=100)
#     branch = models.ForeignKey(Shop,verbose_name=_("branch"),on_delete=models.CASCADE,related_name="gateways",unique=True)

#     class Meta:
#         ordering = ('-pk',)
#         verbose_name = _('Gateway')
#         verbose_name_plural = _('Gateways')

#     def __str__(self):
#         return self.name

#     def get_absolute_url(self):
#         return reverse('app_name_gateway_detail', args=(self.pk,))


#     def get_update_url(self):
#         return reverse('app_name_gateway_update', args=(self.pk,))