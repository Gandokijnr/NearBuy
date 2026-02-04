from django.urls import path
from .views import NearbyStoreView, StripeWebhookView, MeView, OrderListView, OrderLocationUpdateView, OrderDetailView, OrderAcceptView, OrderDeliverView

urlpatterns = [
    path('stores/nearby/', NearbyStoreView.as_view(), name='nearby-stores'),
    path('stripe/webhook/', StripeWebhookView.as_view(), name='stripe-webhook'),
    path('me/', MeView.as_view(), name='me'),
    path('orders/', OrderListView.as_view(), name='orders'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:pk>/location/', OrderLocationUpdateView.as_view(), name='order-location'),
    path('orders/<int:pk>/accept/', OrderAcceptView.as_view(), name='order-accept'),
    path('orders/<int:pk>/deliver/', OrderDeliverView.as_view(), name='order-deliver'),
    path('driver/orders/<int:pk>/', OrderDetailView.as_view(), name='driver-order-detail'),
    path('driver/orders/<int:pk>/location/', OrderLocationUpdateView.as_view(), name='driver-order-location'),
    path('driver/orders/<int:pk>/accept/', OrderAcceptView.as_view(), name='driver-order-accept'),
    path('driver/orders/<int:pk>/deliver/', OrderDeliverView.as_view(), name='driver-order-deliver'),
]
