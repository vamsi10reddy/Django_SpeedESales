from django.contrib import admin
from .models import CartOrder, CartOrderItems, Address

class CartOrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'price', 'paid_status', 'product_status', 'order_date')

class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'qty', 'unit_price', 'total_price')
    list_filter =  ('order',)

class AddressAdmin(admin.ModelAdmin):
    list_display = ('user','order','send_to','address','city','zipCode','status')
    list_filter = ('user','order')

admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderItems, CartOrderItemsAdmin)
admin.site.register(Address, AddressAdmin)
