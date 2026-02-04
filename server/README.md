NearBuy Backend (Django + DRF + GeoDjango + Channels)
=====================================================

This folder contains a Django backend for the NearBuy delivery platform.

Stack
- Django 5, DRF, GeoDjango (PostGIS), Channels (ASGI websockets)
- Stripe webhook -> Django Signal -> Channels broadcast to merchants

Quick start (Windows-friendly via Docker for PostGIS)
1) Python env
   - Python 3.11+ recommended
   - Create venv and install requirements:
     - py -m venv .venv && .venv\Scripts\activate
     - pip install -r requirements.txt
   - Note: GeoDjango requires GEOS/GDAL/PROJ on your system. For easiest setup on Windows, use WSL (Ubuntu) or install OSGeo4W. For development, you can still run with PostGIS via Docker.

2) PostGIS DB (Docker)
   - cd server
   - docker compose up -d
   - Set DATABASE_URL to something like: postgis://postgres:postgres@localhost:5432/nearbuy

3) Configure environment
   - Copy .env.example to .env and adjust values

4) Initialize DB
   - python manage.py makemigrations
   - python manage.py migrate
   - python manage.py createsuperuser

5) Run dev server (ASGI)
   - daphne -b 0.0.0.0 -p 8000 nearbuy_backend.asgi:application
   - Or for HTTP-only testing: python manage.py runserver 0.0.0.0:8000

Endpoints
- GET /api/stores/nearby/?lat=<lat>&lng=<lng>&dist=<km>
- POST /api/stripe/webhook/  (set STRIPE_WEBHOOK_SECRET)
- GET /api/me/  (very simple auth probe)
- GET /api/orders/?status=<status>&store=<id>&driver=<id>&customer=<id>
- WebSocket: ws://<host>/ws/merchant/orders/

Admin
- /admin/  (OSM map on Store model via OSMGeoAdmin)
- /admin/live-orders/ (simple live order monitor via Channels)

Stripe Webhook -> Signal -> Channels
- Stripe webhook (payment_intent.succeeded) triggers `payment_succeeded` signal with the matching Order.
- Signal handler serializes order and broadcasts to group 'merchants'.
- MerchantOrdersConsumer listens on that group and forwards messages to connected websockets.

Notes on GeoDjango on Windows
- GeoDjango requires GEOS/GDAL/PROJ runtime libraries. Easiest path is using WSL (Ubuntu) and installing via apt, or installing OSGeo4W and ensuring DLLs are on PATH.
- Alternatively, develop in a Linux container.

Security
- ALLOWED_HOSTS should be set for production.
- Consider Redis channel layer in production (update CHANNEL_LAYERS).

