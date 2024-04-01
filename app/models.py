from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Create your models here.


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']


class Product(models.Model):
    name = models.CharField(max_length = 50, null=True)
    price = models.FloatField()
    image = models.ImageField(null=True, blank=True)
    brand = models.CharField(max_length=50, null=True)
    detail = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.name
    @property
    def ImageURL(self):
        try:
            url= self.image.url
        except:
            url = ''
        return url
    
    
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True, null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length= 100, null=True)

    def __str__(self):
        return str(self.id)
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
     
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL, blank=False, null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL, blank=False, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=False)
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        if self.product:
            return self.product.price * self.quantity
        return 0
  

class Shipping(models.Model):
    customer = models.ForeignKey(User,on_delete=models.SET_NULL, blank=False, null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL, blank=False, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    State = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.address

class Files(models.Model):
    file = models.FileField(upload_to='file')   