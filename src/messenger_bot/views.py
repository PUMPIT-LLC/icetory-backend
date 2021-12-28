import json

import telebot.types
from django.http import HttpRequest, JsonResponse

from messenger_bot.services.bot import bot


def handle_hook(request: HttpRequest):
    if request.method == "POST" and request.content_type == "application/json":
        data = json.loads(request.body)
        upd = telebot.types.Update.de_json(data)
        bot.process_new_updates([upd])
    return JsonResponse({"success": True})
