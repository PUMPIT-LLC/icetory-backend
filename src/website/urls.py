from django.urls import path

from website.views import ProductViewSet, CategoryViewSet, OrderView, FeedbackView, ReviewViewSet, StoriesViewSet

urlpatterns = [
    # content
    path("reviews/", ReviewViewSet.as_view({"get": "list"})),
    path("stories/", StoriesViewSet.as_view({"get": "list"})),
    # food
    path("categories/", CategoryViewSet.as_view({"get": "list"})),
    path("products/", ProductViewSet.as_view({"get": "list"})),
    # interaction
    path("feedback/", FeedbackView.as_view()),
    path("orders/", OrderView.as_view()),
]
