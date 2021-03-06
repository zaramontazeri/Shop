# Generated by Django 3.2.5 on 2021-08-03 15:58

from decimal import Decimal
from django.conf import settings
import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('media_app', '0004_image'),
        ('users_info', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscountCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, db_index=True, help_text='It will be fill, if you leave it empty. ex: cz6nX', max_length=64, unique=True)),
                ('percentage', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('maximum_value', models.IntegerField(default=0)),
                ('expire_at', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_status', models.CharField(choices=[('dr', 'Draft'), ('pa', 'Payed')], default='dr', max_length=4, verbose_name='pay_status')),
                ('deliver_status', models.CharField(choices=[('pe', 'Pending'), ('co', 'Confirmed'), ('de', 'Delivered')], default='pe', max_length=4, verbose_name='deliver_status')),
                ('shipping_number', models.CharField(blank=True, max_length=24, null=True)),
                ('sell_source', models.CharField(choices=[('si', 'site'), ('in', 'inplace')], default='si', max_length=4, verbose_name='sell_source')),
                ('total_price', models.DecimalField(blank=True, decimal_places=0, default=Decimal('0.00'), max_digits=19, null=True, verbose_name='total price')),
                ('description', models.CharField(blank=True, max_length=200, null=True, verbose_name='description')),
                ('date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='date')),
                ('shipping_price', models.DecimalField(blank=True, decimal_places=0, default=Decimal('0.00'), max_digits=19, null=True, verbose_name='shipping price')),
                ('vtax', models.DecimalField(blank=True, decimal_places=0, default=Decimal('0.00'), max_digits=19, null=True, verbose_name='value added price')),
                ('address', models.ForeignKey(default='-1', on_delete=django.db.models.deletion.PROTECT, to='users_info.address')),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='customer')),
                ('discount_code', models.ForeignKey(null=True, on_delete=models.SET('deleted'), related_name='payments', to='shop.discountcode')),
            ],
            options={
                'verbose_name': 'Invoice',
                'verbose_name_plural': 'Invoices',
                'ordering': ('-pk',),
            },
        ),
        migrations.CreateModel(
            name='Menuitem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('slug', models.SlugField(allow_unicode=True)),
            ],
        ),
        migrations.CreateModel(
            name='OccasionalDiscount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('percentage', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cover', models.ImageField(blank=True, null=True, upload_to='covers/shop/product')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('menuitem', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.menuitem')),
                ('related_products', models.ManyToManyField(blank=True, null=True, related_name='_shop_product_related_products_+', to='shop.Product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='ProductVariation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_size', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=0, max_digits=10)),
                ('discount_price', models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('occasional_discount', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='occasional_discount_set', to='shop.occasionaldiscount')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variations', to='shop.product')),
            ],
        ),
        migrations.CreateModel(
            name='PromotionCodeStrategy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inventory', models.IntegerField(default=0)),
                ('expire_time', models.IntegerField(default=5)),
                ('is_for_first_order', models.BooleanField(default=False)),
                ('percentage', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('maximum_value', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('slug', models.SlugField(allow_unicode=True)),
                ('phone_numbers', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=20, verbose_name='phone number'), size=None)),
                ('full_address', models.TextField(verbose_name='full address')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('order', models.IntegerField(unique=True, verbose_name='order')),
                ('enable', models.BooleanField(default=True, verbose_name='enable')),
                ('cover', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shops', to='media_app.image')),
                ('header', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='media_app.image')),
            ],
            options={
                'verbose_name': 'Shop Shop',
                'verbose_name_plural': 'Shop Categories',
            },
        ),
        migrations.CreateModel(
            name='WorkingTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('1', 'shanbe'), ('2', 'yekshanbe'), ('3', 'doshanbe'), ('4', 'seshanbe'), ('5', 'charshanbe'), ('6', 'pangshanbe'), ('7', 'jome')], max_length=1, verbose_name='day')),
                ('from_time', models.CharField(max_length=150, verbose_name='from_times')),
                ('to_time', models.CharField(max_length=150, verbose_name='to_times')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='working_times', to='shop.shop', verbose_name='branch')),
            ],
            options={
                'verbose_name': 'Working Time',
                'verbose_name_plural': 'Working Times',
            },
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('refId', models.CharField(max_length=100, verbose_name='trackingCode')),
                ('bankRefId', models.CharField(max_length=100, verbose_name='bankRefId')),
                ('status', models.CharField(choices=[('success', 'Success'), ('failed', 'Failed'), ('pending', 'Pending')], max_length=10, verbose_name='status')),
                ('statusNum', models.IntegerField(verbose_name='status number')),
                ('authority', models.CharField(max_length=20, verbose_name='authority')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='transaction', to='shop.invoice', verbose_name='invoice')),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
                'ordering': ('-pk',),
            },
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seller', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('shop', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.shop')),
            ],
        ),
        migrations.CreateModel(
            name='PromotionalCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, db_index=True, help_text='It will be fill, if you leave it empty. ex: cz6nX', max_length=64, unique=True)),
                ('percentage', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('maximum_value', models.IntegerField(default=0)),
                ('num_of_used', models.IntegerField(default=0, editable=False)),
                ('expire_at', models.DateField()),
                ('disable', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductVariationAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute_value', models.CharField(max_length=150)),
                ('attribute', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='shop.productattribute')),
                ('product_variation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.productvariation')),
            ],
        ),
        migrations.AddField(
            model_name='productvariation',
            name='specifications',
            field=models.ManyToManyField(blank=True, related_name='specifications_to_person', through='shop.ProductVariationAttribute', to='shop.ProductAttribute'),
        ),
        migrations.CreateModel(
            name='ProductReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('confirmed', models.BooleanField(default=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_reviews', to='shop.product')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductGalleryImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=128)),
                ('image', models.ImageField(upload_to='shop/gallery')),
                ('order', models.PositiveIntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_images', to='shop.product')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='OrderedItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField(null=True, verbose_name='quantity')),
                ('unit_base_price', models.DecimalField(decimal_places=0, max_digits=19, verbose_name='unit base price')),
                ('unit_discount_price', models.DecimalField(blank=True, decimal_places=0, max_digits=19, null=True, verbose_name='unit discount price')),
                ('invoice', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='shop.invoice', verbose_name='invoice')),
                ('product_variation_item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='shop.productvariation', verbose_name='product item')),
            ],
            options={
                'verbose_name': 'Ordered Item',
                'verbose_name_plural': 'Ordered Items',
                'ordering': ('-pk',),
            },
        ),
        migrations.AddField(
            model_name='menuitem',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='menu_items', to='shop.shop'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='product_items',
            field=models.ManyToManyField(through='shop.OrderedItem', to='shop.ProductVariation', verbose_name='product items'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='promotional_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.SET('deleted'), related_name='promo_payments', to='shop.promotionalcode'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='seller',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.seller', verbose_name='seller'),
        ),
    ]
