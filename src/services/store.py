"""Helpers for store"""
from typing import Iterable, List

from django.conf import settings

from sberbank.service import BankService
from website.models import CartItem, Order


def calculate_price(cart_items: Iterable[CartItem]) -> int:
    return sum((item.product.discount_price or item.product.price) * item.amount for item in cart_items)


def form_payment_url(order: Order) -> str:
    """Form payment URL and link payment object to Order object"""
    cart_items = order.cartitem_set.prefetch_related("product").all()
    price = calculate_price(cart_items)
    svc = BankService(settings.MERCHANT_KEY)
    payment, url = svc.pay(price, params={'order_id': order.id}, description=f'Оплата заказа №{order.id}')
    order.payment = payment
    order.save()
    return url
