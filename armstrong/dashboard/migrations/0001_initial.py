# Generated by Django 3.2.3 on 2021-10-28 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UpdatedDaily',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('total_gross_sales', models.FloatField()),
                ('total_number_of_customers', models.IntegerField()),
                ('total_sales_egypt', models.FloatField()),
                ('total_sales_qatar', models.FloatField()),
                ('total_sales_bahrain', models.FloatField()),
                ('total_sales_saudi_arabia', models.FloatField()),
                ('total_sales_united_arab_emirates', models.FloatField()),
                ('total_sales_jordan', models.FloatField()),
                ('total_sales_kuwait', models.FloatField()),
                ('total_sales_oman', models.FloatField()),
                ('total_sales_international', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='UpdatedDailyMembershipType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('number_of_students', models.IntegerField()),
                ('total_sales', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='UpdatedDailyPromocode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('promocode_name', models.CharField(max_length=255)),
                ('total_sales', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='UpdatedMonthly',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('total_gross_sales', models.FloatField()),
                ('total_number_of_customers', models.IntegerField()),
                ('total_number_of_registers', models.IntegerField()),
            ],
        ),
    ]
