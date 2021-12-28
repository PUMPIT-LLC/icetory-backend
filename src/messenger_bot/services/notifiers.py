"""New order/feedback notifier"""
import telebot
from telebot import types

from messenger_bot.models import BotUser
from messenger_bot.services.decorators import log_any_exception
from services.store import calculate_price
from website.models import Order, FeedbackComment


@log_any_exception()
def notify_new_order(order: Order, bot: telebot.TeleBot):
    users_to_notify = BotUser.objects.filter(chat_id__isnull=False, notifies_on=True).all()
    cart_items = order.cartitem_set.prefetch_related("product").all()
    order_price = calculate_price(cart_items)
    message = "\n".join(
        (
            f"Поступил новый заказ: №{order.id}",
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
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(types.InlineKeyboardButton("Принять заказ", callback_data=f"order::confirm::{order.id}"))
    keyboard.add(types.InlineKeyboardButton("Это спам", callback_data=f"order::spam::{order.id}"))
    for user in users_to_notify:
        bot.send_message(chat_id=user.chat_id, text=message, reply_markup=keyboard)


@log_any_exception()
def notify_new_feedback(feedback: FeedbackComment, bot: telebot.TeleBot):
    users_to_notify = BotUser.objects.filter(chat_id__isnull=False, notifies_on=True).all()
    message = f"Отзыв от {feedback.name}:\n{feedback.message}\n\nКонтактный номер: {feedback.phone}"
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton("Удалить", callback_data=f"feedback::delete::{feedback.id}"))
    for user in users_to_notify:
        bot.send_message(chat_id=user.chat_id, text=message, reply_markup=keyboard)
