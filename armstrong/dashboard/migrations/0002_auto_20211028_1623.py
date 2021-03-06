# Generated by Django 3.2.3 on 2021-10-28 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='updateddaily',
            options={'verbose_name_plural': 'Daily Sales Reports'},
        ),
        migrations.AlterModelOptions(
            name='updateddailymembershiptype',
            options={'verbose_name_plural': 'Daily Memberships Reports'},
        ),
        migrations.AlterModelOptions(
            name='updateddailypromocode',
            options={'verbose_name_plural': 'Daily Promocode Reports'},
        ),
        migrations.AlterModelOptions(
            name='updatedmonthly',
            options={'verbose_name_plural': 'Monthly Sales Reports'},
        ),
        migrations.RemoveField(
            model_name='updateddailymembershiptype',
            name='number_of_students',
        ),
        migrations.AddField(
            model_name='updateddailymembershiptype',
            name='name',
            field=models.CharField(default='One Student', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='updatedmonthly',
            name='date',
            field=models.DateField(),
        ),
    ]
