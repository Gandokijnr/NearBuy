from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.db.models.functions import Cast
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.db.models import GeometryField
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404

from .models import Store, Order
from .serializers import StoreSerializer, UserSerializer, OrderSerializer
from .signals import payment_succeeded


class NearbyStoreView(APIView):
    """Return stores within ?dist (km) of ?lat & ?lng"""
    def get(self, request):
        try:
            lat = float(request.GET.get('lat'))
            lng = float(request.GET.get('lng'))
        except (TypeError, ValueError):
            return Response({'detail': 'lat and lng are required'}, status=400)
        try:
            dist_km = float(request.GET.get('dist', 5))
        except ValueError:
            dist_km = 5.0

        p = Point(lng, lat, srid=4326)
        qs = Store.objects.annotate(distance=Distance('location', p))\
            .filter(location__distance_lte=(p, D(km=dist_km)))\
            .order_by('distance')
        data = StoreSerializer(qs, many=True).data
        # Attach distance_km if available
        for idx, obj in enumerate(qs):
            try:
                data[idx]['distance_km'] = round(obj.distance.km, 3)
            except Exception:
                pass
        return Response(data)


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        payload = request.body.decode('utf-8') if isinstance(request.body, (bytes, bytearray)) else (request.body or '')
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        endpoint_secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', '')
        if not endpoint_secret:
            return Response({'detail': 'Webhook secret not configured'}, status=400)
        try:
            event = stripe.Webhook.construct_event(payload=payload, sig_header=sig_header, secret=endpoint_secret)
        except Exception as e:
            return Response({'detail': f'Invalid payload/signature: {e}'}, status=400)

        if event['type'] == 'payment_intent.succeeded':
            obj = event['data']['object']
            order = None
            order_id = None
            try:
                order_id = obj.get('metadata', {}).get('order_id')
            except Exception:
                order_id = None
            if order_id:
                try:
                    order = Order.objects.get(pk=order_id)
                except Order.DoesNotExist:
                    order = None
            if not order:
                pi_id = obj.get('id')
                if pi_id:
                    order = Order.objects.filter(stripe_payment_intent=pi_id).first()
            if order:
                payment_succeeded.send(sender=self.__class__, order=order, stripe_object=obj)
        return Response({'ok': True})


class MeView(APIView):
    def get(self, request):
        u = request.user if request.user.is_authenticated else None
        data = UserSerializer(u).data if u else {
            'id': None,
            'username': '',
            'email': '',
            'is_merchant': False,
            'is_driver': False,
            'phone': ''
        }
        return Response(data)


class OrderListView(APIView):
    """Very simple order list with ?status= filter and optional ?store, ?driver, ?customer"""
    def get(self, request):
        qs = Order.objects.all().order_by('-created_at')
        status_param = request.GET.get('status')
        if status_param:
            qs = qs.filter(status=status_param)
        for key, field in [('store', 'store_id'), ('driver', 'driver_id'), ('customer', 'customer_id')]:
            val = request.GET.get(key)
            if val:
                qs = qs.filter(**{field: val})
        ser = OrderSerializer(qs[:200], many=True)
        return Response(ser.data)


class OrderLocationUpdateView(APIView):
    """Update the live driver location for an order"""
    def post(self, request, pk: int):
        try:
            lat = float(request.data.get('lat'))
            lng = float(request.data.get('lng'))
        except (TypeError, ValueError):
            return Response({'detail': 'lat and lng are required'}, status=400)

        order = get_object_or_404(Order, pk=pk)
        point = Point(lng, lat, srid=4326)
        order.driver_location = point
        order.save(update_fields=['driver_location', 'updated_at'])
        return Response({'ok': True})


class OrderDetailView(APIView):
    def get(self, request, pk: int):
        order = get_object_or_404(Order, pk=pk)
        return Response(OrderSerializer(order).data)

    def patch(self, request, pk: int):
        order = get_object_or_404(Order, pk=pk)
        new_status = request.data.get('status') or request.data.get('order_status')
        if new_status and new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
        if 'driver' in request.data:
            order.driver_id = request.data.get('driver') or None
        order.save()
        return Response(OrderSerializer(order).data)


class OrderAcceptView(APIView):
    def post(self, request, pk: int):
        order = get_object_or_404(Order, pk=pk)
        order.status = Order.STATUS_OUT
        try:
            if request.user.is_authenticated and getattr(request.user, 'is_driver', False):
                order.driver = request.user
        except Exception:
            pass
        order.save()
        return Response(OrderSerializer(order).data)


class OrderDeliverView(APIView):
    def post(self, request, pk: int):
        order = get_object_or_404(Order, pk=pk)
        order.status = Order.STATUS_COMPLETED
        order.save(update_fields=['status', 'updated_at'])
        return Response(OrderSerializer(order).data)
