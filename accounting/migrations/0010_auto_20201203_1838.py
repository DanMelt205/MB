# Generated by Django 3.1.3 on 2020-12-03 18:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounting', '0009_auto_20201203_1838'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ('-transaction_date',)},
        ),
    ]