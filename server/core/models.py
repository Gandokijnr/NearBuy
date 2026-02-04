from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models as gis_models
from django.db import models


class User(AbstractUser):
    is_merchant = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)
    phone = models.CharField(max_length=32, blank=True, default='')

    def __str__(self) -> str:
        return self.username or self.email or f"user:{self.pk}"


class Store(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stores')
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=255, blank=True, default='')
    location = gis_models.PointField(geography=True, srid=4326)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    image = models.URLField(blank=True, default='')

    def __str__(self) -> str:
        return f"{self.name} ({self.store_id})"


class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_PREPARING = 'preparing'
    STATUS_READY = 'ready_for_pickup'
    STATUS_OUT = 'out_for_delivery'
    STATUS_COMPLETED = 'completed'
    STATUS_REJECTED = 'rejected'
    STATUS_CHOICES = [
        (STATUS_NEW, 'New'),
        (STATUS_PREPARING, 'Preparing'),
        (STATUS_READY, 'Ready for Pickup'),
        (STATUS_OUT, 'Out for Delivery'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='orders')
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='customer_orders')
    driver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='driver_orders')

    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=STATUS_NEW)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    service_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    pickup_location = gis_models.PointField(geography=True, srid=4326, null=True, blank=True)
    dropoff_location = gis_models.PointField(geography=True, srid=4326, null=True, blank=True)
    driver_location = gis_models.PointField(geography=True, srid=4326, null=True, blank=True)

    customer_phone = models.CharField(max_length=32, blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    stripe_payment_intent = models.CharField(max_length=200, blank=True, default='')

    def __str__(self) -> str:
        return f"order:{self.pk}"


class Transaction(models.Model):
    TYPE_PAYMENT = 'payment'
    TYPE_REFUND = 'refund'
    TYPE_CHOICES = [
        (TYPE_PAYMENT, 'Payment'),
        (TYPE_REFUND, 'Refund'),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=TYPE_PAYMENT)
    stripe_id = models.CharField(max_length=200, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"txn:{self.pk}:{self.type}:{self.amount}"
