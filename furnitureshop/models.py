from django.db import models
from django.contrib.auth.models import User


# Create your models here.



# settings.py ma AUTH_USER_MODEL="furnitureshop.Customer"
















class Customer(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name=models.CharField(max_length=200)
    address=models.CharField(max_length=200,null=True,blank=True)
    joint_on=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.full_name



class Catagory(models.Model):
    title=models.CharField(max_length=200)
    slug=models.SlugField(unique=True)
    def __str__(self):
         return self.title

class Product(models.Model):
    title=models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    catagory=models.ForeignKey(Catagory,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='pics')
    marked_price=models.PositiveIntegerField()
    selling_price=models.PositiveIntegerField()
    description=models.TextField()
    discount=models.BooleanField(default=False)
    return_policy=models.CharField(max_length=200,null=True,blank=True)
    view_count=models.PositiveIntegerField(default=0)

    def __str__(self):
         return self.title

class Cart(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    total_amout=models.PositiveIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Cart :"+ str(self.id)
class Cartproduct(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    rate=models.PositiveIntegerField()
    quantaty=models.PositiveIntegerField()
    subtotal=models.PositiveIntegerField(default=0)
    def __str__(self):
        return "Cart :"+ str(self.cart.id) +"CartProduct: " + str(self.id)

ORDER_STATUS= {
    ("Order Received", "Order Received "),
    ("Order Processing", "Order Processing"),
    ("On The Way", "On The Way"),
    ("Order Completed", "Order Completed")

}

class Order(models.Model):
    cart=models.OneToOneField(Cart,on_delete=models.CASCADE)
    order_by=models.CharField(max_length=200)
    shipping_address=models.CharField(max_length=200)
    mobile=models.CharField(max_length=20)
    email=models.EmailField(null=True,blank=True)
    subtotal=models.PositiveIntegerField(default=0)
    discount=models.PositiveIntegerField(default=0)
    total=models.PositiveIntegerField(default=0)
    order_status=models.CharField(max_length=50,choices=ORDER_STATUS)
    created_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Order :" + str(self.id)




class Message(models.Model):
    name=models.CharField(max_length=100)
    email= models.EmailField(max_length=100,blank=True)
    phone= models.CharField(max_length=30)
    message= models.TextField(max_length=500)

    def __str__(self):
        return self.name




