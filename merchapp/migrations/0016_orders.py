# Generated by Django 5.0.1 on 2024-01-27 13:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchapp', '0015_products_totalsells'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderid', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('pid', models.ForeignKey(db_column='pid', on_delete=django.db.models.deletion.CASCADE, to='merchapp.products')),
                ('uid', models.ForeignKey(db_column='userid', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
