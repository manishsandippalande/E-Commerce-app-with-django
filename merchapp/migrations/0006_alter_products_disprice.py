# Generated by Django 5.0.1 on 2024-01-19 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchapp', '0005_alter_products_disprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='disprice',
            field=models.IntegerField(blank=True, default=models.IntegerField()),
        ),
    ]
