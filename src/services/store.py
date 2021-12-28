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
    payment, url = svc.pay(price, params={"order_id": order.id}, description=f"Оплата заказа №{order.id}")
    order.payment = payment
    order.save()
    return url


def form_order_text_repr(order: Order, report_prefix: str) -> str:
    """
    report_prefix is used to handle context:
    either this report is for customer eyes or a manager
    """
    cart_items = order.cartitem_set.prefetch_related("product").all()
    order_price = calculate_price(cart_items)
    return "\n".join(
        (
            f"{report_prefix}: №{order.id}",
            "",
            f"От: {order.name}",
            "",
            "Контакты:",
            f"Телефон: {order.phone}",
            f"E-mail: {order.email}",
            "",
            f"Сумма заказа: {order_price}",
            f"Способ оплаты: {order.payment_type}",
            "" "Дата доставки:",
            f"{order.day} в интервале {order.delivery_time}",
            "",
            "Адрес доставки:",
            ", ".join(
                filter(
                    lambda x: x,
                    (
                        f"{order.address}",
                        f"подъезд {order.entrance}" if order.entrance else "",
                        f"квартира {order.apartment}",
                        f"этаж {order.floor}",
                        f"домофон {order.intercom}" if order.intercom else "",
                    ),
                )
            ),
            f"Комментарий: {order.comment}" if order.comment else "",
            "",
            "Позиции заказа:",
            "\n".join(f"{item.product} - {item.amount} шт." for item in cart_items),
        )
    )
