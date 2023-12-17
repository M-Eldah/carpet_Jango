from rest_framework import serializers
from .models import ProductCategory, Product, ProductImg, ProductSizes,Material



class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductImg
        fields=(
            "image",
            "url",
            "url_Thumbnail"
        )

class SizesSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductSizes
        fields=(
            "product",
            "Sizes",
            "amount",
            "productid",
            "price"
        )
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
       
        model=Product
        fields=(
            "id",
            "name",
            "slug",
            "material",
            "get_absolute_url",
            "description",
            "price",
            "get_thumbnail",
            "get_material",
            "get_type",
            "productsizes",
            "productimgs",
            "count"
        )
        
class CategorySerializer(serializers.ModelSerializer):
    """ products = ProductSerializer(many=True) """
    class Meta:
        model = ProductCategory
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "products",
            "productCount"
        )
        
class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model=Material
        fields=(
            "id",
            "name",
            "get_absolute_url",
            "products",
            "productCount"
        )