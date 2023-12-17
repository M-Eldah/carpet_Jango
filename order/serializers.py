from rest_framework import serializers
from .models import order_detail,order_item
from product.serializers import ProductSerializer
from product.models import Product

class Myorder_item_serializer(serializers.ModelSerializer):
    product=ProductSerializer()
    class Meta:
        model=order_item
        fields=('price','product','quantity','size',)
class order_item_serializer(serializers.ModelSerializer):

    class Meta:
        model=order_item
        fields=('price','product','quantity','size',)

class Myorder_detail_serializer(serializers.ModelSerializer):
    items=Myorder_item_serializer(many=True)
    class Meta:
        model=order_detail
        fields=(
            'id',
            'first_name',
            'last_name',
            'email',
            'address',
            'zipcode',
            'items',
            'phone',
            'ordertotal'
        )
 


class order_detail_serializer(serializers.ModelSerializer):
    items=order_item_serializer(many=True)
    class Meta:
        model=order_detail
        fields=(
            'id',
            'first_name',
            'last_name',
            'email',
            'address',
            'zipcode',
            'items',
            'phone',
            'ordertotal',
            'ExtraNotes'
        )
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = order_detail.objects.create(**validated_data)

        for item_data in items_data:
            order_item.objects.create(order=order, **item_data)
            
        return order
        