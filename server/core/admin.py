from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.safestring import mark_safe
from django.contrib.gis.admin import OSMGeoAdmin

from .models import User, Store, Product, Order, Transaction


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "is_staff", "is_merchant", "is_driver")
    search_fields = ("username", "email")
    list_filter = ("is_staff", "is_merchant", "is_driver")


@admin.register(Store)
class StoreAdmin(OSMGeoAdmin):
    list_display = ("id", "name", "owner")
    search_fields = ("name",)
    default_lon = 0
    default_lat = 0
    default_zoom = 2


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "store", "price", "in_stock")
    list_filter = ("in_stock",)
    search_fields = ("name",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "store", "customer", "driver", "status", "total", "created_at")
    list_filter = ("status", "store")
    search_fields = ("id",)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "type", "amount", "stripe_id", "created_at")
    list_filter = ("type",)


@staff_member_required
def live_orders(request):
    context = {
        "title": "Live Orders",
    }
    return TemplateResponse(request, "core/live_orders.html", context)
