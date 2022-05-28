# Generated by Django 3.2.5 on 2021-08-07 18:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.AlterModelOptions(
            name='shop',
            options={'verbose_name': 'Shop ', 'verbose_name_plural': 'Shop Categories'},
        ),
        migrations.AddField(
            model_name='invoice',
            name='delivery_type',
            field=models.CharField(choices=[('in', 'inplace'), ('ta', 'taxi')], default='ta', max_length=4, verbose_name='deliver_status'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='seller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.seller', verbose_name='seller'),
        ),
        migrations.CreateModel(
            name='ShopSubCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suppliers', to='shop.shopcategory')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.AddField(
            model_name='shop',
            name='subcategory',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='suppliers', to='shop.shopsubcategory'),
            preserve_default=False,
        ),
    ]