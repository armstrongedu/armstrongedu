# Generated by Django 3.2.3 on 2021-10-28 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_auto_20211028_1623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='updatedmonthly',
            name='date',
            field=models.CharField(max_length=255),
        ),
    ]
