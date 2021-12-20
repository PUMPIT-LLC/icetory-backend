from django.urls import path

from website.views import ProductViewSet, CategoryViewSet, OrderView

urlpatterns = [
    # food
    path("categories/", CategoryViewSet.as_view({"get": "list"})),
    # path('discounts/', ),
    path("products/", ProductViewSet.as_view({"get": "list"})),
    # # interaction
    # path('feedback/', ),
    path("orders/", OrderView.as_view()),
]
