from django.contrib import admin

from .models import BillingData, Membership, Card, Invoice, CardToken, MembershipType, Promocode


@admin.register(MembershipType)
class MembershipTypeAdmin(admin.ModelAdmin):
    list_display = ('plan', 'country', 'name', 'display_float_price', 'real_price_egyptian_cents', 'std_display_float_price', 'std_real_price_egyptian_cents',)


@admin.register(BillingData)
class BillingDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'address_1', 'city', 'state', 'postal_code', 'country', 'phone', 'email',)


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'activated_on', 'get_status_display', 'membership_type', 'number_of_students',)


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('user', 'card_type', 'last_4_digits',)


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('user', 'card', 'paymob_id', 'created_at', 'item_name', 'item_price', 'promocode_price', 'billed', 'add_stds_price',)


@admin.register(CardToken)
class CardTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token',)

@admin.register(Promocode)
class PromocodeTypeAdmin(admin.ModelAdmin):
    list_display = ('promocode', 'percent',)

