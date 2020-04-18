from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

USER_TYPES=[
    ('VR','vendor'),
    ('CR','customer'),
    ('AD','admin')
]

class Profile(models.Model):
    user_type=models.CharField(choices=USER_TYPES, max_length=2)
    user=models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Vendor_profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    company_name=models.CharField(max_length=100, blank=True)
    address=models.CharField(max_length=300, blank=True)
    phone=models.CharField(max_length=13, blank=True)
    acc_number=models.CharField(max_length=20, blank=True)
    ifsc_code=models.CharField(max_length=15, blank=True)
    bank=models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.user.username


class Store(models.Model):
    name=models.CharField(max_length=100)
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    description=models.CharField(max_length=100, blank=True)
    slug=models.SlugField(max_length=200,blank=True)
    title=models.CharField(max_length=100, default="Untitled")
    subtitle=models.CharField(max_length=100, default="Small subtitle")


    def __str__(self):
        return f"Owner: {self.owner.username} | {self.name}"

    

class Product(models.Model):
    store=models.ForeignKey(Store, on_delete=models.CASCADE)
    product_name=models.CharField(max_length=100)
    manufacturer=models.CharField(max_length=200)
    image_url=models.TextField(null=True,blank=True)
    quantity=models.IntegerField(default=1)
    price=models.FloatField()
    stock=models.IntegerField()
    sales_count=models.IntegerField()
    description=models.TextField(max_length=100)
    rating=models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        return f"{self.product_name} | {self.store.name}"


class Customer(models.Model):

    name=models.CharField(max_length=100)
    address=models.CharField(max_length=300)
    phone=models.CharField(max_length=13)
    email=models.CharField(max_length=50, null=True)
    
    def __str__(self):
        return self.name

class Order(models.Model):
    store=models.ForeignKey(Store, on_delete=models.CASCADE, null=True)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE, null=True )
    timestamp=models.DateTimeField(auto_now_add=True)
    is_shipped=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)

    def __str__(self):
        return f"#{self.id}|Customer:{self.customer.name} |{self.store}"

class OrderItem(models.Model):
    order=models.ForeignKey(Order, on_delete=models.CASCADE,null=True,related_name="order_items")
    product=models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity=models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product.product_name} x {self.quantity} |#{self.order_id}"

class Cart(models.Model):
    ssid=models.CharField(max_length=300)
    store=models.ForeignKey(Store,on_delete=models.CASCADE )
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.store}"


class CartItem(models.Model):
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now_add=True)
    quantity= models.IntegerField(default=1)
    def __str__(self):
        return self.product.product_name

