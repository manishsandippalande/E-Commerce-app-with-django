# Generated by Django 5.0.1 on 2024-02-02 16:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchapp', '0020_registrationdata'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registrationdata',
            name='user_data',
        ),
    ]
