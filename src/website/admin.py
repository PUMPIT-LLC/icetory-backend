from django.contrib import admin

# Register your models here.
from website.models import Product, Category, Order, CartItem, FeedbackComment


@admin.register(FeedbackComment)
class FeedbackAdmin(admin.ModelAdmin):
    readonly_fields = ("name", "phone", "message", "created_at")


class CartItemAdmin(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ("product",)
    fields = ("product", "amount")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (CartItemAdmin,)
    readonly_fields = ("name", "phone", "email", "created_at")


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(CartItem)
