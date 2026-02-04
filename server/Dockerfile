FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System deps for GeoDjango (GDAL/GEOS/PROJ) and build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    gdal-bin libgdal-dev libgeos-dev proj-bin libproj-dev \
    gcc build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps first (better layer caching)
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# Copy app source
COPY . /app

EXPOSE 8000

# Run migrations then start ASGI server (Channels)
CMD ["sh", "-c", "python manage.py migrate && daphne -b 0.0.0.0 -p 8000 nearbuy_backend.asgi:application"]
