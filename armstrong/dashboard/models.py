from django.db import models


class UpdatedDaily(models.Model):
    date = models.DateField(auto_now=True)
    total_gross_sales = models.FloatField(null=False, blank=False)
    total_number_of_customers = models.IntegerField(null=False, blank=False)
    total_sales_egypt = models.FloatField(null=False, blank=False)
    total_sales_qatar = models.FloatField(null=False, blank=False)
    total_sales_bahrain = models.FloatField(null=False, blank=False)
    total_sales_saudi_arabia = models.FloatField(null=False, blank=False)
    total_sales_united_arab_emirates = models.FloatField(null=False, blank=False)
    total_sales_jordan = models.FloatField(null=False, blank=False)
    total_sales_kuwait = models.FloatField(null=False, blank=False)
    total_sales_oman = models.FloatField(null=False, blank=False)
    total_sales_international = models.FloatField(null=False, blank=False)

    def __str__(self):
        return str(date)

    class Meta:
        verbose_name_plural = "Daily Sales Reports"


class UpdatedMonthly(models.Model):
    date = models.CharField(max_length=255)
    total_gross_sales = models.FloatField(null=False, blank=False)
    total_number_of_customers = models.IntegerField(null=False, blank=False)
    total_number_of_registers = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return str(date)

    class Meta:
        verbose_name_plural = "Monthly Sales Reports"

class UpdatedDailyPromocode(models.Model):
    date = models.DateField(auto_now=True)
    promocode_name = models.CharField(max_length=255, null=False, blank=False)
    total_sales = models.FloatField(null=False, blank=False)

    def __str__(self):
        return str(date)

    class Meta:
        verbose_name_plural = "Daily Promocode Reports"

class UpdatedDailyMembershipType(models.Model):
    date = models.DateField(auto_now=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    total_sales = models.FloatField(null=False, blank=False)

    def __str__(self):
        return str(date)

    class Meta:
        verbose_name_plural = "Daily Memberships Reports"
