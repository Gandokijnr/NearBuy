from django.dispatch import Signal, receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Order
from .serializers import OrderSerializer

# Fired when Stripe webhook confirms payment success
payment_succeeded = Signal()  # args: order, stripe_object


@receiver(payment_succeeded)
def on_payment_succeeded(sender, order: Order, stripe_object=None, **kwargs):
    # Optionally update order or log, then notify merchants via Channels
    try:
        data = OrderSerializer(order).data
    except Exception:
        data = {'id': getattr(order, 'id', None)}
    channel_layer = get_channel_layer()
    if channel_layer:
        async_to_sync(channel_layer.group_send)(
            'merchants',
            {
                'type': 'order.event',
                'order': data,
            },
        )
