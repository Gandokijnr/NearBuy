import math
from typing import Tuple, Dict


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def calculate_fees(
    store_coords: Tuple[float, float],
    user_coords: Tuple[float, float],
    base_fee: float = 2.5,
    per_km_rate: float = 1.2,
    service_pct: float = 0.05,
    min_service_fee: float = 0.5,
) -> Dict[str, float]:
    """
    Calculate delivery_fee and service_fee between store and user coordinates.
    Returns dict: { 'distance_km', 'delivery_fee', 'service_fee' }
    """
    slat, slng = store_coords
    ulat, ulng = user_coords
    distance_km = haversine_km(slat, slng, ulat, ulng)
    delivery_fee = base_fee + per_km_rate * max(distance_km, 0.0)
    service_fee = max(min_service_fee, service_pct * delivery_fee)
    return {
        'distance_km': round(distance_km, 3),
        'delivery_fee': round(delivery_fee, 2),
        'service_fee': round(service_fee, 2),
    }
