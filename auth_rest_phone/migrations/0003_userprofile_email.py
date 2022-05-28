# Generated by Django 3.1.1 on 2020-09-30 10:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_rest_phone', '0002_auto_20200921_2010'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.CharField(max_length=150, null=True, validators=[django.core.validators.EmailValidator(code='invalid_email')]),
        ),
    ]