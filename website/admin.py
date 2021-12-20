from django.contrib import admin

# Register your models here.
from website.models import Product, Category, Order, CartItem


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(CartItem)
