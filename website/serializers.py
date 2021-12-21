from rest_framework import serializers

from website.models import Product, Category, Order, FeedbackComment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class CartItemSerializer(serializers.Serializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    amount = serializers.IntegerField(min_value=1)


class OrderSerializer(serializers.ModelSerializer):
    cart = CartItemSerializer(many=True)

    class Meta:
        model = Order
        exclude = ["created_at"]


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackComment
        exclude = ["created_at"]
