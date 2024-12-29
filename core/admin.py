from django.contrib import admin
from core.models import Category, Product
from .models import Category, Product, Vendor#,ProductImages

# Register your models here.
'''
class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages
'''
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category_image')

class ProductAdmin(admin.ModelAdmin):
    #inlines = [ProductImagesAdmin]
    list_display = ('title', 'user','image', 'price', 'featured', 'product_status')
    list_filter = ('date', 'in_stock', 'user')

class VendorAdmin(admin.ModelAdmin):
    list_display = ('title', 'vendor_image')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Vendor, VendorAdmin)