from django.db import models
from django.contrib.auth.models import User
import uuid
from slugify import slugify



class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=500, null=True)
    ip = models.CharField(max_length=200, null=True, blank=True)
    date_added = models.DateTimeField('created', auto_now_add=True, null=True, blank=True)
    date_uploaded = models.DateTimeField('modified', auto_now=True, null=True, blank=True)
    def __str__(self):
        return str(self.name)

class Product(models.Model):
    title = models.CharField(max_length=500, null=True)
    name = models.CharField(max_length=100, null=True)
    link = models.CharField(max_length=500, null=True, blank=True, default=uuid.uuid1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='static/img/products/', null=True, blank=True)
    date_added = models.DateTimeField('created', auto_now_add=True, null=True, blank=True)
    date_uploaded = models.DateTimeField('modified', auto_now=True, null=True, blank=True)
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.link = slugify(self.title)
        super(Product, self).save(*args, **kwargs)



class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True)
    date_added = models.DateTimeField('created', auto_now_add=True, null=True, blank=True)
    date_uploaded = models.DateTimeField('modified', auto_now=True, null=True, blank=True)
    def __str__(self):
        if self.customer is not None:
            return str(self.id) + str(self.customer.name) + "'s order"
        else:
            return str(self.id) + " : order"

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField('created', auto_now_add=True, null=True, blank=True)
    date_uploaded = models.DateTimeField('modified', auto_now=True, null=True, blank=True)
    is_current = models.BooleanField(default=True, null=True, blank=True)
    def __str__(self):
        return str(self.id)

    def quantity_price(self):
        return float(self.quantity * self.product.price)

class ShippingAdress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=300, null=True)
    city = models.CharField(max_length=50, null=True)
    zipcode = models.CharField(max_length=10, null=True)
    date_added = models.DateTimeField('created', auto_now_add=True, null=True, blank=True)
    date_uploaded = models.DateTimeField('modified', auto_now=True, null=True, blank=True)
    def __str__(self):
        if self.customer is not None:
            return str(self.customer) + ' : ' + str(self.address)
        else:
            return str(self.id) + ' ' + ' :  ' + str(self.address)

class Portfolio(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    ip = models.CharField(max_length=20, null=True, blank=True)
    date_added = models.DateTimeField('created', auto_now_add=True, null=True, blank=True)
    def __str__(self):
        return self.name
