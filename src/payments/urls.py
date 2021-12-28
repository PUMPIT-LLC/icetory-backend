from django.urls import path

from payments.views import payment_success, payment_fail

urlpatterns = [
    path("success", payment_success),
    path("fail", payment_fail)
]
