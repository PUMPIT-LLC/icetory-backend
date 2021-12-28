from django.db import transaction
from rest_framework import viewsets, views
from rest_framework.response import Response

from messenger_bot.services.bot import bot
from messenger_bot.services.notifiers import notify_new_order, notify_new_feedback
from website.models import Product, Category, FeedbackComment, CartItem, Order, ClientReview, VideoStory
from website.serializers import (
    ProductSerializer,
    CategorySerializer,
    OrderSerializer,
    FeedbackSerializer,
    ReviewSerializer,
    VideoStorySerializer,
)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = ClientReview.objects.all()
    serializer_class = ReviewSerializer


class StoriesViewSet(viewsets.ModelViewSet):
    queryset = VideoStory.objects.all()
    serializer_class = VideoStorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderView(views.APIView):
    http_method_names = ["post"]

    # pylint: disable-next=no-self-use
    @transaction.atomic
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = serializer.validated_data.pop("cart")
        order = Order(**serializer.validated_data)
        order.save()
        CartItem.objects.bulk_create(
            [CartItem(order=order, product=item["product_id"], amount=item["amount"]) for item in cart]
        )
        notify_new_order(order, bot)
        return Response()


class FeedbackView(views.APIView):
    http_method_names = ["post"]

    # pylint: disable-next=no-self-use
    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_feedback_comment = FeedbackComment(**serializer.validated_data).save()
        notify_new_feedback(new_feedback_comment, bot)
        return Response()
