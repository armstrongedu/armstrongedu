# Generated by Django 3.2.3 on 2021-12-30 01:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0018_invoice_add_stds_price'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invoice',
            options={'ordering': ('-created_at',)},
        ),
    ]
