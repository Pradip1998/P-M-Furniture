from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,UserManager
from django.utils.translation import gettext as _

# Create your models here.



# settings.py ma AUTH_USER_MODEL="furnitureshop.Customer"




class CustomUserManager(UserManager):
    def _create_user(self, username, email, password, **extra_fields):

        if not username:
            raise ValueError('The given username must be set.')

        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must  have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username, email, password, **extra_fields)


class Customer(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer.'),
        validators=[username_validator],
        error_messages={
            'unique': _('A user with the username already exits.')
        }
    )
    email = models.EmailField(_("email address"), max_length=254, unique=True, default='test@gmail.com')
    full_name=models.CharField(max_length=200)
    address=models.CharField(max_length=200,null=True,blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether user can log into admin or not.')
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates wheter this should be treated as active'
            'Unselect this instead of deleting accounts.'
        )
    )
    date_joined = models.DateTimeField(_('date_joined'), default=timezone.now)
    email_varified = models.BooleanField(
        _('email_varified'),
        default=False,
        help_text=_('Designates whether users email is varified.')
    )
    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']





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


class ProdctImage(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='pics')
    def __str__(self):
         return self.product




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
class Happycustomer(models.Model):
    name=models.CharField(max_length=100)
    post=models.CharField(max_length=100)
    image = models.ImageField(upload_to='pics')
    description= models.TextField(max_length=500)
    def __str__(self):
        return self.name




