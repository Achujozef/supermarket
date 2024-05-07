from django.db import models
from django.contrib.auth.models import User

class Shop(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    pincode = models.CharField(max_length=10)
    logo = models.ImageField(upload_to='shop_logos/', blank=True, null=True)
    owner_name = models.CharField(max_length=100)
    owner_contact = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE,default=0)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        print('delete Called')
        Product.objects.filter(category=self).update(category=None)
        super(Category, self).delete(*args, **kwargs)

class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/CustomerProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    name=models.CharField(max_length=40)
    product_image= models.ImageField(upload_to='product_image/',null=True,blank=True)
    price = models.PositiveIntegerField()
    quantity = models.CharField(max_length=40)
    description = models.TextField()
    def __str__(self):
        return self.name
    
class Address(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    full_address = models.CharField(max_length=200)
    pincode = models.CharField(max_length=10)

    def __str__(self):
        return self.full_address


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Order Confirmed', 'Order Confirmed'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
    )
    status = models.CharField(max_length=50, null=True, choices=STATUS)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order {self.pk}"

class Orders(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    

    def __str__(self):
        return f"OrderItem {self.pk}"

class Feedback(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE,default=0)
    name=models.CharField(max_length=40)
    feedback=models.CharField(max_length=500)
    date= models.DateField(auto_now_add=True,null=True)
    def __str__(self):
        return self.name
