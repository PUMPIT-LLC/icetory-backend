from django.conf import settings
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from messenger_bot.views import handle_hook

urlpatterns = [
    # CHANGE
    path(settings.WEBHOOK_URL.split('/')[-1].strip(), csrf_exempt(handle_hook)),
]
