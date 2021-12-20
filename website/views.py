from rest_framework import viewsets, views
from rest_framework.response import Response

from website.models import Product, Category
from website.serializers import ProductSerializer, CategorySerializer, OrderSerializer


class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class OrderView(views.APIView):
    http_method_names = ["post"]

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({})
