import asyncio
from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status,authentication,permissions
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.response import Response
from order.models import order_detail
from product.serializers import SizesSerializer
from product.models import ProductSizes,Product
from .serializers import order_detail_serializer,Myorder_detail_serializer,Myorder_item_serializer
from notificationapi_python_server_sdk import (notificationapi)

@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def checkout(request):
    serializer=order_detail_serializer(data=request.data)
    if serializer.is_valid():
        paid_amount=sum(item.get('quantity')*item.get('price') for item in serializer.validated_data['items'])
        print(paid_amount)
        checkout=True
        error=[]
        for item in serializer.validated_data['items']:
            size=ProductSizes.objects.filter(product__id=item.get('product').id).filter(Sizes=item.get('size')).values('product','amount',)
            storageAmm=size[0].get('amount')
            orderAmm=item['quantity']
            if(storageAmm<orderAmm):
                checkout=False
                newe = f'The quantity of {item.get("product").name} in size {item.get("size")} in stock isn\'t enough to cover your order we only have {storageAmm } pieces in stock'
                error.append(newe)

        if(checkout):
            serializer.save(user=request.user,ordertotal=paid_amount)
            order=''
            for item in serializer.validated_data['items']:
                size=ProductSizes.objects.filter(product__id=item.get('product').id).filter(Sizes=item.get('size')).values('product','amount',)
                storageAmm=size[0].get('amount')
                orderAmm=item['quantity']
                order = order + f'{item.get("product").name}, size: {item.get("size")}, Quantity {orderAmm} ||'
                size.update(amount=storageAmm-orderAmm)
            print(order)
            name=request.user
            notificationapi.init(
                "1faqpagr970v528lond6aopnq5",  # clientId
                "1kcahcql5oabrkcsorknhcilvf99bjepdvms7s6onnkia2v098mk" # clientSecret
            )
            asyncio.run(
                notificationapi.send({
                    "notificationId": "welcome",
                    "templateId": "notification_mail",
                    "user": {
                            "id": "test_user_id",
                            "email": "mohamedahmedeldah@gmail.com"
                    }, 
                    "mergeTags": { 
                    "UserName": f'{name}',
                    "order": f'{order}'
                    }
                })
            )
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            print('Failure')
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
    else:
        print('Failure2')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class OrdersList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        orders = order_detail.objects.filter(user=request.user)
        serializer = Myorder_detail_serializer(orders, many=True)
        return Response(serializer.data)
    