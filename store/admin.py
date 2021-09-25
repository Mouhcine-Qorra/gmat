from django.contrib import admin
from .models import *




class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'email', 'ip', 'date_added', 'date_uploaded')
    readonly_fields = ["date_added", "date_uploaded"]

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'name', 'price', 'image', 'date_added', 'date_uploaded')
    readonly_fields = ["date_added", "date_uploaded"]

class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ('product', 'images', 'date_added', 'date_uploaded')
    readonly_fields = ["date_added", "date_uploaded"]

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'date_ordered', 'complete', 'transaction_id', 'date_added', 'date_uploaded')
    readonly_fields = ["date_added", "date_uploaded"]

class ItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'quantity', 'to_order', 'date_added', 'date_uploaded')
    readonly_fields = ["date_added", "date_uploaded"]

class ShippingAdmin(admin.ModelAdmin):
    list_display = ('customer', 'order', 'address', 'city', 'zipcode', 'date_added', 'date_uploaded')
    readonly_fields = ["date_added", "date_uploaded"]

class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'email', 'message', 'ip', 'date_added')
    readonly_fields = ["date_added"]

admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage, ProductImagesAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, ItemAdmin)
admin.site.register(ShippingAdress, ShippingAdmin)
admin.site.register(Portfolio, PortfolioAdmin)
