from django.db import models
from io import BytesIO
from PIL import Image
from django.core.files import File

# Create your models here.
#Categories for the product.


class ProductCategory(models.Model):
    name=models.CharField(max_length=255)
    slug=models.SlugField()
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return f'/{self.slug}/'
    
    def productCount(self) -> int:
        return 1
    
class Material(models.Model):
    name=models.CharField(max_length=255)
    slug=models.SlugField()
    
    class Meta:
        ordering = ('name',)
    
    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return f'/{self.slug}/'
    
    def productCount(self) -> int:
        return 1
    
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    category= models.ForeignKey(ProductCategory,related_name='products',on_delete=models.CASCADE)
    material= models.ForeignKey(Material,related_name='products',on_delete=models.CASCADE)
    name=models.CharField(max_length=255)
    slug=models.SlugField(unique=True)
    description=models.TextField(blank=True,null=True)
     
    thumbnail=models.ImageField(upload_to='uploads/',blank=True)
    
    
    location=models.CharField(max_length=255,default='Storage')
    data_added=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-data_added',)
    
    def __str__(self) -> str:
        return self.name
    def price(self):
        return 100
    def get_material(self)  -> str:
        return self.material.name
    def count(self):
        return 0
    def get_type(self)  -> str:
        return self.category.name
    
    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'
    
    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        return ''
       
class ProductSizes(models.Model):
    product=models.ForeignKey(Product,related_name='productsizes',on_delete=models.CASCADE)
    Sizes=models.CharField(max_length=255,default='Storage')
    amount=models.IntegerField()
    price=models.DecimalField(max_digits=9,decimal_places=2)   
    class Meta:
        ordering = ('-product',)
        verbose_name = 'Size'
        verbose_name_plural = 'Sizes'
    def __str__(self) -> str:
        return self.product.name + ' - ' + self.Sizes
    def productid(self):
        return self.product.id
    
class ProductImg(models.Model):
    product=models.ForeignKey(Product,related_name='productimgs',on_delete=models.CASCADE)
    image=models.ImageField(upload_to='uploads/',blank=True,null=True)
    thumbnail=models.ImageField(upload_to='uploads/',blank=True)
    
    class Meta:
        ordering = ('-product',)
        verbose_name = 'Images'
        verbose_name_plural = 'Images'
    def __str__(self) -> str:
        return self.product.name + ' - ' + self.image.name
    
    def url(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''
    
    def url_Thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            self.thumbnail=self.makeThumb(self.image)
            self.save()
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        return ''
    
    def makeThumb(self, image,size=(100,100)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)
        thumb_io=BytesIO()
        img.save(thumb_io,'PNG',quality=80)
        
        thumbnail=File(thumb_io,name=image.name)
        return thumbnail