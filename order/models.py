from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from product.models import Product

class order_detail(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,related_name='orders',on_delete=models.CASCADE)
    first_name = models.CharField(max_length=199)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=256)
    address = models.TextField(blank=True,null=True)
    ExtraNotes = models.TextField(blank=True,null=True)
    zipcode = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    prePaid=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    Cost=models.DecimalField(max_digits=50,decimal_places=2,blank=True,null=True),
    newOrder=models.BooleanField(default=True)
    ordertotal=models.DecimalField(max_digits=9,decimal_places=2)
    class Meta: 
        ordering = ['-created_at',]
        
    def __str__(self) :
        return "Order id:"+str(self.id)+"_User"+self.first_name

class order_item(models.Model):
    id = models.AutoField(primary_key=True)
    order=models.ForeignKey(order_detail,related_name='items',on_delete=models.CASCADE)
    product=models.ForeignKey(Product,related_name="order_items",on_delete=models.CASCADE)
    price=models.DecimalField(max_digits=9,decimal_places=2)
    size=models.CharField(max_length=100)
    quantity=models.IntegerField(default=1)
    
    class Meta: 
        ordering = ['-order__created_at',]
    def __str__(self) :
        return "Order id:"+str(self.order.id)+"_item:"+str(self.product.id)
    