from django.urls import path
from .consumers import MerchantOrdersConsumer

websocket_urlpatterns = [
    path('ws/merchant/orders/', MerchantOrdersConsumer.as_asgi()),
]
