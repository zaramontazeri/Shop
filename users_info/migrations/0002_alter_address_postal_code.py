# Generated by Django 3.2.5 on 2021-08-07 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_info', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='postal_code',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
    ]
