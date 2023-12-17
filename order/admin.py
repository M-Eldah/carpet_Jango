from django.contrib import admin
from .models import order_detail,order_item
# Register your models here.

class OrderDetailAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = ["id","user", "email","phone","ordertotal","newOrder"]
    list_filter = ["user","newOrder"]

class OrderItemAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = ["order","product", "size","quantity"]
    list_filter = ["order"]
admin.site.register(order_detail, OrderDetailAdmin)
admin.site.register(order_item,OrderItemAdmin)