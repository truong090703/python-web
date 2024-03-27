from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True,blank=False)
    name = models.CharField(max_length = 50, null=True)
    email = models.CharField(max_length = 50, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length = 50, null=True)
    price = models.FloatField()
    image = models.ImageField(null=True, blank=True)

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
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL,blank=True, null=True)
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
        total = self.product.price * self.quantity
        return total   

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

# from django.db import models
# from django.utils import timezone
# # Create your models here.
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm

# class CreateUserForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['username','email','first_name','last_name','password1','password2']

# # class Customer(models.Model):
# #     id = models.AutoField(primary_key=True)
# #     User = models.OneToOneField(User, on_delete=models.SET_NULL,null=True, blank=False)
# #     name = models.CharField(max_length=200,null=True)
# #     email = models.CharField(max_length=200,null=True)
    
# #     def __str__(self):
# #         return self.name
# class Category(models.Model):
#     sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name='sub_categories', null=True, blank=True)
#     is_sub = models.BooleanField(default=False)
#     name = models.CharField(max_length=200, null=True)
#     slug = models.SlugField(max_length=200, unique=True)

#     def __str__(self):
#         return self.name
    
# class Product(models.Model):
#     category = models.ManyToManyField(Category,related_name='product')
#     name = models.CharField(max_length=200,null=True)
#     price = models.FloatField()
#     # digital = models.BooleanField(default=False,null=True, blank=False)
#     image = models.ImageField(null=True, blank=True)
#     # created_at = models.DateTimeField(default=timezone.now)
    
#     def __str__(self):
#         return self.name
    
#     @property
#     def ImageURL(self):
#         try:
#             url= self.image.url
#         except:
#             url = ''
#         return url
# class Order(models.Model):
#     customer = models.ForeignKey(User,on_delete=models.SET_NULL, blank=False, null=True)
#     date_order = models.DateTimeField(auto_now_add=True) 
#     complete = models.BooleanField(default=False,null=True,blank=False)
#     transaction_id = models.CharField(max_length=200, null=True)
    
#     def __str__(self):
#         return str(self.id)
#     @property
#     def get_cart_items(self):
#         order_items = self.order_item_set.all()
#         total = sum([item.quantity for item in order_items])
#         return total
    
#     @property
#     def get_cart_total(self):
#         order_items = self.order_item_set.all()
#         total = sum([item.get_total for item in order_items])
#         return total
    
# class Order_item(models.Model):
#     product = models.ForeignKey(Product,on_delete=models.SET_NULL, blank=False, null=True)
#     order = models.ForeignKey(Order,on_delete=models.SET_NULL, blank=False, null=True)
#     quantity = models.IntegerField(default=0, null=True, blank=False)
#     date_added = models.DateTimeField(auto_now_add=True)
    
#     @property
#     def get_total(self):
#         total = self.product.price * self.quantity
#         return total    
# class Shipping(models.Model):
#     customer = models.ForeignKey(User,on_delete=models.SET_NULL, blank=False, null=True)
#     order = models.ForeignKey(Order,on_delete=models.SET_NULL, blank=False, null=True)
#     address = models.CharField(max_length=200, null=True)
#     city = models.CharField(max_length=200, null=True)
#     State = models.CharField(max_length=200, null=True)
#     mobile = models.CharField(max_length=200, null=True)
#     date_added = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return self.address