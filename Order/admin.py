from django.contrib import admin
from .models import *
# Register your models here.


class WishlistAdmin(admin.ModelAdmin):
    list_display = ['product', 'user']
    list_filter = ['user']

admin.site.register(Wishlist, WishlistAdmin)

class ShippingChargeAdmin(admin.ModelAdmin):
    list_display = ['city', 'charge']

admin.site.register(ShippingCharge, ShippingChargeAdmin)


class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'qty', 'price', 'amount']
    list_filter = ['user']

admin.site.register(ShopCart, ShopCartAdmin)

class ShopCartDeviceAdmin(admin.ModelAdmin):
    list_display = ['product', 'device', 'qty', 'price', 'amount']
    list_filter = ['device']

admin.site.register(ShopCartDevice, ShopCartDeviceAdmin)


class OrderProductline(admin.TabularInline):
    model = OderProduct
    readonly_fields = ('product', 'user' , 'price', 'qty', 'amount')
    can_delete = False
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name',
                    'phone', 'total', 'status', 'transaction_id']
    list_filter = ['status']
    readonly_fields = ('user', 'first_name', 'last_name',
                       'phone', 'address', 'city', 'country', 'total', 'ip', 'transaction_id', 'image_tag')
    can_delete = False
    inlines = [OrderProductline]

admin.site.register(Order, OrderAdmin)


class OrderProductAdmin(admin.ModelAdmin):
    list_display = ['status', 'user', 'product', 'price', 'qty', 'amount']
    list_filter = ['user']



admin.site.register(OderProduct, OrderProductAdmin)
