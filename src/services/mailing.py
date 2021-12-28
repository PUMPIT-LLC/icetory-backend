import logging

from django.core.mail import send_mail, get_connection as django_get_connection
from django.conf import settings

from services.store import form_order_text_repr
from website.models import Order

log = logging.getLogger(__name__)


class MissingConnectionException(Exception):
    pass


def get_connection(label=None, **kwargs):
    if label is None:
        label = getattr(settings, "EMAIL_CONNECTION_DEFAULT", None)

    try:
        connections = getattr(settings, "EMAIL_CONNECTIONS")
        options = connections[label]
    except (KeyError, AttributeError):
        raise MissingConnectionException('Settings for connection "%s" were not found' % label)

    options.update(kwargs)
    return django_get_connection(**options)


def send_order_via_email(order: Order):
    """Send E-mail to a person who ordered this thing"""
    message = form_order_text_repr(order, "Мы получили Ваш заказ")
    try:
        with get_connection("store") as connection:
            send_mail('Заказ "icetory"', message, settings.EMAIL_HOST, [order.email], connection=connection)
    except Exception as e:
        log.critical(f"Failed to send order email: {e}")
