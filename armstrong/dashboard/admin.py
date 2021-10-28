from django.contrib import admin

from .models import UpdatedDaily, UpdatedMonthly,UpdatedDailyPromocode, UpdatedDailyMembershipType


@admin.register(UpdatedDaily)
class UpdatedDailyAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'total_gross_sales',
        'total_number_of_customers',
        'total_sales_egypt',
        'total_sales_qatar',
        'total_sales_bahrain',
        'total_sales_saudi_arabia',
        'total_sales_united_arab_emirates',
        'total_sales_jordan',
        'total_sales_kuwait',
        'total_sales_oman',
        'total_sales_international',
    )


@admin.register(UpdatedMonthly)
class UpdatedMonthlyAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'total_gross_sales',
        'total_number_of_customers',
        'total_number_of_registers',
    )


@admin.register(UpdatedDailyPromocode)
class UpdatedDailyPromocodeAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'promocode_name',
        'total_sales',
    )


@admin.register(UpdatedDailyMembershipType)
class UpdatedDailyMembershipTypeAdmin(admin.ModelAdmin):
    list_display = (
        'date',
        'name',
        'total_sales',
    )

