import math
import decimal
import geopy.distance
from .common import (
    is_all_numeric,
    is_list_or_tuple,
    is_numeric
)

def get_bounding_box(latitude_in_degrees, longitude_in_degrees, half_side_in_km):
    if half_side_in_km <= 0:
        raise AssertionError
    if not (latitude_in_degrees >= -90.0 and latitude_in_degrees <= 90.0):
        raise AssertionError
    if not (longitude_in_degrees >= -180.0 and longitude_in_degrees <= 180.0):
        raise AssertionError

    lat = math.radians(latitude_in_degrees)
    lng = math.radians(longitude_in_degrees)

    radius  = 6371
    # Radius of the parallel at given latitude
    parallel_radius = radius*math.cos(lat)

    lat_min = lat - half_side_in_km/radius
    lat_max = lat + half_side_in_km/radius
    lng_min = lng - half_side_in_km/parallel_radius
    lng_max = lng + half_side_in_km/parallel_radius
    rad2deg = math.degrees

    box = {
        'lat_min': decimal.Decimal(rad2deg(lat_min)),
        'lat_max': decimal.Decimal(rad2deg(lat_max)),
        'lng_min': decimal.Decimal(rad2deg(lng_min)),
        'lng_max': decimal.Decimal(rad2deg(lng_max)),
    }

    return box

def get_boundingboxes_incremental_steps(
    lat,
    lng,
    steps_m = None,
    exclude_prev_step_inner = True
):
    if steps_m is None:
        steps_m = [100, 250, 500, 1000, 2500]
    if not is_all_numeric([lat, lng]):
        return None

    (lat, lng) = (float(lat),float(lng))

    if not is_list_or_tuple(steps_m):
        if is_numeric(steps_m):
            km = steps_m/1000
            return [get_bounding_box(lat, lng, km),]
        return None

    if not is_all_numeric(steps_m): return None
    
    boundingboxes = {}
    steps_m = sorted(steps_m)

    for i, m in enumerate(steps_m):
        key = str(m)
        km = m/1000

        boundingboxes[key] = {
            'boundingbox': get_bounding_box(lat,lng,km),
        }

        if exclude_prev_step_inner and i > 0:
            prev_km = steps_m[(i-1)]/1000
            boundingboxes[key]['exclude_inner'] = get_bounding_box(lat,lng,prev_km)

    return boundingboxes

# def calculate_distance(latlng1,latlng2):
#   return geopy.distance.distance(latlng1,latlng2)