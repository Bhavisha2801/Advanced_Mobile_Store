from django.db import models
from django.contrib.auth.models import User


# Create your models here.

# Create your models here.
class MainCategoryModel(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to ='MainCategory')
    info  = models.CharField(max_length=200)


    def __str__(self):
        return self.name

class SubCategoryModel(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to ='subCategory')
    info  = models.CharField(max_length=200)


    def _(self):
        return self.name




st= (('New-Arrival','New-Arrival'),('Out-of-Stock','Out-of-Stock'))
class ProductModel(models.Model):
    mcate = models.ForeignKey(MainCategoryModel,on_delete=models.CASCADE)
    scate = models.ForeignKey(SubCategoryModel,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to = 'Product',null=True,blank=True)
    image1 = models.ImageField(upload_to = 'Product',null=True,blank=True)
    image2 = models.ImageField(upload_to = 'Product',null=True,blank=True)
    image3 = models.ImageField(upload_to = 'Product',null=True,blank=True)
    og_price = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    discounted_price = models.IntegerField(default=0)
    sell_price = models.IntegerField(default=0)
    info = models.TextField()
    status = models.CharField(max_length=200,choices=st,default='New-Arrival')
    total_price = models.IntegerField(default=0)



    def __str__(self):
        return self.name

    def dis_price(self):
        return (self.og_price * self.discount)/100

    def s_price(self):
        return (self.og_price - self.dis_price())

    def save(self, *args, **kwargs):
        self.discounted_price = self.dis_price()
        self.sell_price = self.s_price()
        super(ProductModel, self).save(*args, **kwargs)


class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    def total(self):
        return ((self.product.sell_price)*(self.quantity))  





class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone_number = models.IntegerField()
    city = models.CharField(max_length=100)
    def __str__(self):
        return self.name


Status = (
            ("Order Accepted","Order Accepted"),
            ("confirm order","confirm order")
            )


class Myorder(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=25,choices=Status,default="pending")
    def _str_(self):
        return self.user.username


   

