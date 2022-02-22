from django.contrib import admin

# Register your models here.
from website.models import Product, Category, Order, CartItem, FeedbackComment, VideoStory, ClientReview, ProductImage


@admin.register(FeedbackComment)
class FeedbackAdmin(admin.ModelAdmin):
    readonly_fields = ("name", "phone", "message", "created_at")


class CartItemAdmin(admin.TabularInline):
    model = CartItem
    extra = 0
    fields = ("product", "amount")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_filter = ("status",)
    inlines = (CartItemAdmin,)
    readonly_fields = ("name", "phone", "email", "created_at", "payment")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("position", "title")
    ordering = ("position",)


admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(ProductImage)
admin.site.register(ClientReview)
admin.site.register(VideoStory)
