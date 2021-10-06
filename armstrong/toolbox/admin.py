from django.contrib import admin

from .models import ToolBox, Order


@admin.register(ToolBox)
class ToolBoxAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('bosta_id', 'user', 'toolbox',)
