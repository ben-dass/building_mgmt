# Generated by Django 5.1.6 on 2025-02-16 18:20

import phonenumber_field.modelfields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="phone_number",
            field=phonenumber_field.modelfields.PhoneNumberField(
                blank=True,
                default="+12125552368",
                max_length=30,
                null=True,
                region=None,
                verbose_name="Phone Number",
            ),
        ),
    ]
