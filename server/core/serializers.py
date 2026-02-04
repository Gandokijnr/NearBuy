from rest_framework import serializers
from django.contrib.gis.geos import Point
from .models import User, Store, Product, Order, Transaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_merchant', 'is_driver', 'phone']


class StoreSerializer(serializers.ModelSerializer):
    lat = serializers.SerializerMethodField()
    lng = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = ['id', 'name', 'address', 'lat', 'lng']

    def get_lat(self, obj):
        try:
            return obj.location.y
        except Exception:
            return None

    def get_lng(self, obj):
        try:
            return obj.location.x
        except Exception:
            return None


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'store', 'name', 'price', 'in_stock', 'image']


class OrderSerializer(serializers.ModelSerializer):
    store_name = serializers.ReadOnlyField(source='store.name')
    driver_payout = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    store_lat = serializers.SerializerMethodField()
    store_lng = serializers.SerializerMethodField()
    pickup = serializers.SerializerMethodField()
    dropoff = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'store', 'store_name', 'customer', 'driver', 'status',
            'subtotal', 'delivery_fee', 'service_fee', 'total',
            'customer_phone', 'created_at', 'updated_at',
            'stripe_payment_intent', 'driver_payout',
            'store_lat', 'store_lng', 'pickup', 'dropoff'
        ]

    def get_store_lat(self, obj):
        try:
            if obj.pickup_location:
                return obj.pickup_location.y
        except Exception:
            pass
        try:
            return obj.store.location.y
        except Exception:
            return None

    def get_store_lng(self, obj):
        try:
            if obj.pickup_location:
                return obj.pickup_location.x
        except Exception:
            pass
        try:
            return obj.store.location.x
        except Exception:
            return None

    def get_pickup(self, obj):
        try:
            if obj.pickup_location:
                return {'lat': obj.pickup_location.y, 'lng': obj.pickup_location.x}
        except Exception:
            pass
        try:
            # fallback to store location
            if obj.store and obj.store.location:
                return {'lat': obj.store.location.y, 'lng': obj.store.location.x}
        except Exception:
            pass
        return None

    def get_dropoff(self, obj):
        try:
            if obj.dropoff_location:
                return {'lat': obj.dropoff_location.y, 'lng': obj.dropoff_location.x}
        except Exception:
            pass
        return None


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'order', 'amount', 'type', 'stripe_id', 'created_at']
