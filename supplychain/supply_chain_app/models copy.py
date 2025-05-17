

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Default user ID function
def get_default_user_id():
    return User.objects.first().id if User.objects.exists() else None

class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories_user', default=get_default_user_id)  # Ensure default is set to the function

    def __str__(self):
        return self.name

class Goods(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goods_user', default=get_default_user_id)  # Ensure default is set to the function
    name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True, related_name='goods')
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, null=True, blank=True, related_name='goods')
    date_added = models.DateTimeField(auto_now_add=True)
    barcode = models.CharField(max_length=255, default="000000")

    def __str__(self):
        return self.name

    def total_value(self):
        return self.price * self.quantity

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customers_user', default=get_default_user_id)  # Ensure default is set to the function
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
