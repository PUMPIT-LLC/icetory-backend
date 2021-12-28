import logging

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.request import Request

log = logging.getLogger(__name__)


@api_view(http_method_names=["GET"])
def payment_success(request: Request):
    log.info("Payment successful")
    return HttpResponse()


@api_view(http_method_names=["GET"])
def payment_fail(request: Request):
    log.info("Payment failed")
    return HttpResponse()
