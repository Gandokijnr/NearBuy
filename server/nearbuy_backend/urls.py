from django.contrib import admin
from django.urls import path, include
from core.admin import live_orders

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/live-orders/', live_orders, name='admin-live-orders'),
    path('api/', include('core.urls')),
]
