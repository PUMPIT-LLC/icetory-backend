from rest_framework import serializers

from website.models import Product, Category, Order, FeedbackComment, ClientReview, VideoStory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    main_picture = serializers.SerializerMethodField()
    extra_picture = serializers.SerializerMethodField()

    def get_main_picture(self, obj):
        if not obj.main_picture:
            return None
        return self.context["request"].build_absolute_uri(obj.main_picture.image.url)

    def get_extra_picture(self, obj):
        if not obj.extra_picture:
            return None
        return self.context["request"].build_absolute_uri(obj.extra_picture.image.url)

    class Meta:
        model = Product
        fields = "__all__"


# pylint: disable-next=abstract-method
class CartItemSerializer(serializers.Serializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    amount = serializers.IntegerField(min_value=1)


class OrderSerializer(serializers.ModelSerializer):
    cart = CartItemSerializer(many=True)

    class Meta:
        model = Order
        exclude = ["created_at", "status"]


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackComment
        exclude = ["created_at"]


class VideoStorySerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    def get_url(self, obj):
        return self.context["view"].request.build_absolute_uri(obj.video.url)

    class Meta:
        model = VideoStory
        exclude = ["id", "video"]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientReview
        exclude = ["id"]
