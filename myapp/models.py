from django.db import models
from django.contrib.auth.models import AbstractUser
from decimal import Decimal
from ckeditor.fields import RichTextField
from django.utils import timezone
# Create your models here.


class User(AbstractUser):
    phone = models.CharField(max_length=10, null=True)
    address = models.CharField(max_length=255,blank=True, null=True)
    avatar = models.ImageField(upload_to="uploads/users/%Y/%m",blank=True, null=True)

class Category(models.Model):
    name = models.CharField(max_length= 100, unique= True)
    create_at = models.DateTimeField(auto_now_add= True)
    update_at = models.DateTimeField(auto_now= True)
    active = models.BooleanField(default= True)

    def __str__(self):
        return self.name

class Products(models.Model):
    class Meta:
        unique_together = ("name","category")
    name = models.CharField(max_length= 255)    
    description = RichTextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add= True)
    update_at = models.DateTimeField(auto_now= True)
    category = models.ForeignKey(Category, on_delete= models.CASCADE)

    def __str__(self):
        return self.name
    

class ProductImage(models.Model):
    image = models.ImageField(upload_to="uploads/producs/%Y/%m")
    product = models.ForeignKey(Products, related_name="images", on_delete= models.CASCADE)

    def __str__(self):
        return f"Ảnh của {self.product.name}"

class Cart(models.Model):
    user = models.ForeignKey(User,null=True, blank=True, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40, null=True, blank =True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Cart {self.id}'
    
    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete = models.CASCADE)
    product = models.ForeignKey(Products, on_delete= models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.product.name} ({self.quantity})'
    
    @property
    def total_price(self):
        return Decimal(self.product.sale_price) * self.quantity


class Order(models.Model):
    tinh_trang = [
        ("cxn", "Chờ xác nhận"),
        ("clh", "Chờ lấy hàng"),
        ("cgh", "Chờ giao hàng"),
        ("dg", "Đã giao"),
        ("dh", "Đã hủy"),
    ]
    PAYMENT_METHOD_CHOICES = [
        ("cod", "Thanh toán khi nhận hàng"),
        ("wallet", "Thanh toán qua ví điện tử"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=tinh_trang, default="cxn")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_status = models.CharField(max_length=50, default='Chưa thanh toán')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default="cod")
    order_code = models.CharField(max_length=100, unique=True, default="DEFAULT_CODE")

    def save(self, *args, **kwargs):
        if self.order_code == "DEFAULT_CODE":
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            self.order_code = f'DH-{timestamp}-{self.user.id}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Order {self.order_code}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'OrderItem: {self.product.name} ({self.quantity})'

class Slide(models.Model):
    title = models.CharField(max_length= 100,blank=True, null=True)
    content = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to="uploads/slide/%Y/%m")
    active = models.BooleanField(default= True)

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = RichTextField()
    image = models.ImageField(upload_to="uploads/posts/%Y/%m")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default= True)

    def __str__(self):
        return self.title

