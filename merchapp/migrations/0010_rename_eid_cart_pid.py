# Generated by Django 5.0.1 on 2024-01-23 14:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchapp', '0009_cart'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='eid',
            new_name='pid',
        ),
    ]