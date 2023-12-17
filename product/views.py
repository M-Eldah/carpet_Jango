import asyncio
from telnetlib import STATUS
import time
from django.http import Http404
from django.db.models import Count,Q,Subquery,OuterRef
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Product,ProductCategory,Material
from .models import ProductImg,ProductSizes
from .serializers import ProductSerializer,ImageSerializer,SizesSerializer,CategorySerializer,MaterialSerializer


# Create your views here.

class LatestProductsList(APIView):
    def get(self,request, format=None):
        productList=Product.objects.annotate(count=Count(Subquery(ProductSizes.objects.filter(product__id=OuterRef('id'),amount__gt=0).values('amount')))).annotate(price=Subquery(ProductSizes.objects.filter(product__id=OuterRef('id'),amount__gt=0).values('price'))).filter(count__gt=0)[0:4]       
        serializer=ProductSerializer(productList,many=True)
        return Response(serializer.data)
    
    
class ProductDetail(APIView):
    def get_object(self,category_slug,product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404
    
    def get(self,request,category_slug,product_slug,format=None):
        product=self.get_object(category_slug,product_slug)
        serialier=ProductSerializer(product)
        productsImg=ProductImg.objects.filter(product__slug=product_slug).all()[0:3]
        serializerImg=ImageSerializer(productsImg,many=True)
        productsize=ProductSizes.objects.filter(product__slug=product_slug).filter(amount__gt=0).all()
        serialiersize=SizesSerializer(productsize,many=True)
        
        Serializer_list = [serialier.data, serializerImg.data,serialiersize.data]

        content = {
        'status': 1, 
        'responseCode' : '202ok', 
        'data': Serializer_list,
        }
        return Response(content)

class Category(APIView):
    def get(self,request, format=None):
        productList=ProductCategory.objects.annotate(productCount=Count('products')).filter(productCount__gt=0)
        serializer=CategorySerializer(productList,many=True)
        return Response(serializer.data)

class FilterData(APIView):
    def get(self,request, format=None):
        productList=ProductCategory.objects.annotate(productCount=Count('products')).filter(productCount__gt=0)
        Catserializer=CategorySerializer(productList,many=True)
        productList2=Material.objects.annotate(productCount=Count('products')).filter(productCount__gt=0)
        Matserializer=MaterialSerializer(productList2,many=True)
        Serializer_list = [Catserializer.data, Matserializer.data]

        content = {
        'status': 1, 
        'responseCode' : '202ok', 
        'data': Serializer_list,
        }
        return Response(content)

class FilterProduct(APIView):
    def get(self,request,category_slug,material_slug,format=None):
        if category_slug=='None' and material_slug=='None':
            productlist=Product.objects.annotate(count=Count(Subquery(ProductSizes.objects.filter(product__id=OuterRef('id'),amount__gt=0).values('amount')))).annotate(price=Subquery(ProductSizes.objects.filter(product__id=OuterRef('id'),amount__gt=0).values('price'))).filter(count__gt=0).all()
            print(1)
        elif category_slug=='None':
            productlist=Product.objects.annotate(count=Count(Subquery(ProductSizes.objects.filter(product__id=OuterRef('id'),amount__gt=0).values('amount')))).annotate(price=Subquery(ProductSizes.objects.filter(product__id=OuterRef('id'),amount__gt=0).values('price'))).filter(count__gt=0).filter(material__slug=material_slug).all()
            print(productlist)
            print(2)
        elif material_slug=='None':
            productlist=Product.objects.annotate(count=Count(Subquery(ProductSizes.objects.filter(product__id=OuterRef('id'),amount__gt=0).values('amount')))).annotate(price=Subquery(ProductSizes.objects.filter(product__id=OuterRef('id'),amount__gt=0).values('price'))).filter(count__gt=0).filter(category__slug=category_slug).all()    
            print(3)
        else:
            productlist=Product.objects.annotate(count=Count(Subquery(ProductSizes.objects.filter(product__id=OuterRef('id'),amount__gt=0).values('amount')))).annotate(price=Subquery(ProductSizes.objects.filter(product__id=OuterRef('id'),amount__gt=0).values('price'))).filter(count__gt=0).filter(category__slug=category_slug,material__slug=material_slug).all()
            print(4)

        serlizer=ProductSerializer(productlist,many=True)
        return Response(serlizer.data)

class ProductImages(APIView):
    def get(self,request,product_slug,format=None):
        products=ProductImg.objects.filter(product__slug=product_slug).all()[0:3]
        serializer=ImageSerializer(products,many=True)
        return Response(serializer.data)

class CategoryDetail(APIView):
    def get_object(self, category_slug):
        try:
            return ProductCategory.objects.get(slug=category_slug)
        except Material.DoesNotExist:
            return Http404
        
    def get(self,request,category_slug,format=None):
        Category=self.get_object(category_slug)
        
        Catseriliazer=CategorySerializer(Category)
        
        productList=Catseriliazer.data['products']
        products=[]
        print(productList)
        for id in productList:
            print(id)
            if ProductSizes.objects.filter(product__id=id).filter(amount__gt=0).values("product").distinct().count()>0:
                products.append(Product.objects.annotate(price=Subquery(ProductSizes.objects.filter(product__id=OuterRef('id'),amount__gt=0).values('price'))).get(id=id))       
        serializer=ProductSerializer(products,many=True)
        
        content = {
        'status': 1, 
        'responseCode' : '202ok', 
        'Products': serializer.data,
        'category': Catseriliazer.data

        }
        return Response(content)
    
@api_view(['POST'])
def search(request):
    query=request.data.get('query','')
    if(query):
        
        Products=Product.objects.filter(Q(name__icontains=query)|Q(description__icontains=query))
        serializer=ProductSerializer(Products,many=True)
        productList=[]
        for p in serializer.data:
            slug=p['slug']
            if ProductSizes.objects.filter(product__slug=slug).filter(amount__gt=0).values("product").distinct().count()>0:
                productList.append(Product.objects.annotate(price=Subquery(ProductSizes.objects.filter(product__id=OuterRef('id'),amount__gt=0).values('price'))).get(slug=slug))
        serializer=ProductSerializer(productList,many=True)
        return Response(serializer.data)
    else :
        return Response({"Prodcuts":''})    