from django.contrib import admin
from .models import Goods, Category, Customer

admin.site.register(Goods)
# admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Customer)