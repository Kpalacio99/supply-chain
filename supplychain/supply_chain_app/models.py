from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()  # Get the custom User model if it's used, otherwise the default Django User model

# Default user ID function
def get_default_user_id():
    # Return the first user's ID if users exist, otherwise return None
    return User.objects.first().id if User.objects.exists() else None

# Category model to store product categories
class Category(models.Model):
    name = models.CharField(max_length=100)  # The name of the category
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories_user', default=get_default_user_id)  # ForeignKey to the User model, ensures categories are linked to users

    def __str__(self):
        return self.name  # Return the name of the category for better representation in the admin or shell

# Goods model to store products
class Goods(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goods_user', default=get_default_user_id)  # ForeignKey to User, ensures the product belongs to a user
    name = models.CharField(max_length=255)  # The name of the product
    quantity = models.IntegerField()  # The quantity of the product in stock
    description = models.TextField(blank=True)  # A text field to describe the product
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Price of the product (with two decimal places)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True, related_name='goods')  # ForeignKey to the Category model (can be blank or null)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, null=True, blank=True, related_name='goods')  # ForeignKey to the Customer model (can be blank or null)
    date_added = models.DateTimeField(auto_now_add=True)  # Automatically records when the product was added
    barcode = models.CharField(max_length=255, default="000000")  # Barcode for the product with a default value of "000000"

    def __str__(self):
        return self.name  # Return the name of the product for easy display in the admin or shell

    def total_value(self):
        # Calculate and return the total value of the product (price * quantity)
        return self.price * self.quantity

# Customer model to store customer details
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customers_user', default=get_default_user_id)  # ForeignKey to User, ensures the customer belongs to a user
    name = models.CharField(max_length=100)  # Customer's name
    email = models.EmailField(blank=True)  # Customer's email (optional)
    phone = models.CharField(max_length=20, blank=True)  # Customer's phone number (optional)
    address = models.TextField(blank=True)  # Customer's address (optional)
    date_added = models.DateTimeField(auto_now_add=True)  # Automatically records when the customer was added

    def __str__(self):
        return self.name  # Return the customer's name for easy display in the admin or shell
