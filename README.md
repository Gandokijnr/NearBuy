NearBuy is a real-time, location-aware delivery platform designed to bridge the gap between busy urban professionals and local neighborhood commerce. Unlike traditional delivery giants, NearBuy focuses on "Zero-Latency Logistics" using spatial data to sync users with the absolute nearest available inventory, reducing delivery times and carbon footprints.

The Technical Summary (The "Engineer" View)

NearBuy is a full-stack, three-tier marketplace (Customer, Merchant, Logistics) architected for speed and scalability:

Geospatial Engine: Leveraging PostGIS and GeoDjango to perform real-time proximity calculations, ensuring users only see stores within an optimal delivery radius.

Reactive Frontend: A mobile-first Progressive Web App (PWA) built with Nuxt 4, utilizing the latest directory structure and useFetch composables for instantaneous UI updates.

Real-time Dispatch: Powered by Django Channels and WebSockets, enabling live order tracking and instant notifications between stores and drivers.

Smart Payments: Integrated with Stripe Connect for automated split-payments, handling platform commissions and vendor payouts in a single transaction.
