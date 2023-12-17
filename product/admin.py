from django.contrib import admin

from .models import ProductCategory,Product,ProductImg,Material,ProductSizes
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = ["name","category", "material", "slug","price"]
    list_filter = ["category", "material"]
class ImgAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_filter = ["product"]
class SizesAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = ["product","Sizes", "amount","price"]
    list_filter = ["product","Sizes","price"]
admin.site.register(ProductCategory)
admin.site.register(Product,ProductAdmin)
admin.site.register(ProductImg,ImgAdmin)
admin.site.register(ProductSizes,SizesAdmin)
admin.site.register(Material)