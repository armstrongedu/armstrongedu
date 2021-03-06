# Generated by Django 3.2.3 on 2021-10-26 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0010_auto_20211026_0805'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promocode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('promocode', models.CharField(max_length=255)),
                ('amount_cents_egypt', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='invoice',
            name='item_name',
            field=models.CharField(default=20, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='invoice',
            name='item_price',
            field=models.IntegerField(default=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='invoice',
            name='promocode_price',
            field=models.IntegerField(default=20),
            preserve_default=False,
        ),
    ]
