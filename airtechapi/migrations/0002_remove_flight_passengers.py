# Generated by Django 2.2.4 on 2019-08-23 15:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('airtechapi', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flight',
            name='passengers',
        ),
    ]
