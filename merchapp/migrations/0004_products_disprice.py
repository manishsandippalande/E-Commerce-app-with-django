# Generated by Django 5.0.1 on 2024-01-19 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchapp', '0003_remove_products_disprice'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='disprice',
            field=models.IntegerField(default=1),
        ),
    ]
