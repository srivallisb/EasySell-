from django.contrib import admin

from stores.models import *

class  CartItemAdmin(admin.ModelAdmin):
    list_display=['cart','product']


admin.site.register(Profile)
admin.site.register(Vendor_profile)
admin.site.register(Store)
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register([Cart, CartItem, OrderItem ])
