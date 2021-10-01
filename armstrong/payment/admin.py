from django.contrib import admin

from .models import BillingData, Membership, Card, Invoice, CardToken


@admin.register(BillingData)
class BillingDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'address_1', 'city', 'state', 'postal_code', 'country', 'phone', 'email',)


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'activated_on', 'get_status_display',)


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('user', 'card_type', 'last_4_digits',)


@admin.register(Invoice)
class InoviceAdmin(admin.ModelAdmin):
    list_display = ('user', 'card', 'paymob_id', 'created_at', 'service', 'billed',)


@admin.register(CardToken)
class CardTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token',)
