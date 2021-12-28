"""New order/feedback notifier"""
import telebot
from telebot import types

from messenger_bot.models import BotUser
from messenger_bot.services.decorators import log_any_exception
from services.store import form_order_text_repr
from website.models import Order, FeedbackComment


@log_any_exception()
def notify_new_order(order: Order, bot: telebot.TeleBot):
    users_to_notify = BotUser.objects.filter(chat_id__isnull=False, notifies_on=True).all()
    message = form_order_text_repr(order, "Поступил новый заказ")
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
