import logging

import telebot
from telebot.types import Message, CallbackQuery, ReplyKeyboardRemove
from django.conf import settings

from messenger_bot.models import BotUser
from messenger_bot.services.decorators import log_any_exception
from website.models import Order, OrderStatus, FeedbackComment

log = logging.getLogger(__name__)

bot = telebot.TeleBot(settings.BOT_TOKEN)

wh_info: telebot.types.WebhookInfo = bot.get_webhook_info()
if wh_info.url != settings.WEBHOOK_URL:
    log.info("Removing webhook")
    bot.remove_webhook()
    log.info("Setting new webhook")
    bot.set_webhook(url=settings.WEBHOOK_URL)


@bot.message_handler(commands=["start"])
@log_any_exception(log=log)
def handle_start_command(message: Message):
    log.error("Start command")
    user_id = message.from_user.id
    user = BotUser.objects.filter(user_id=user_id).first()
    if user is None:
        bot.send_message(chat_id=message.chat.id, text="Пользователь не найден")
        return
    if user.chat_id:
        bot.send_message(chat_id=message.chat.id, text="Вы уже зарегестрированы")
        return
    user.chat_id = message.chat.id
    user.save()


@bot.callback_query_handler(func=lambda x: x.data.startswith("order::confirm::"))
@log_any_exception(log=log)
def confirm_order(call: CallbackQuery):
    log.info("Confirming order")
    # move it to separate func "get_callback_data_id"
    order_id = int(call.data.split("::")[2])
    # move such things to service one day
    order = Order.objects.get(id=order_id)
    order.status = OrderStatus.IN_PROGRESS
    order.save()
    bot.edit_message_reply_markup(
        message_id=call.message.id, chat_id=call.message.chat.id, inline_message_id=call.inline_message_id
    )


@bot.callback_query_handler(func=lambda x: x.data.startswith("order::spam::"))
@log_any_exception(log=log)
def add_order_to_spam(call: CallbackQuery):
    log.info("Adding order to spam")
    order_id = int(call.data.split("::")[2])
    # move such things to service one day
    order = Order.objects.get(id=order_id)
    order.status = OrderStatus.SPAM
    order.save()
    bot.edit_message_reply_markup(
        message_id=call.message.id, chat_id=call.message.chat.id, inline_message_id=call.inline_message_id
    )


@bot.callback_query_handler(func=lambda x: x.data.startswith("feedback::delete::"))
@log_any_exception(log=log)
def delete_feedback(call: CallbackQuery):
    log.info("Deleting feedback")
    feedback_id = int(call.data.split("::")[2])
    comment = FeedbackComment.objects.get(id=feedback_id)
    comment.delete()
    bot.edit_message_reply_markup(
        message_id=call.message.id, chat_id=call.message.chat.id, inline_message_id=call.inline_message_id
    )
