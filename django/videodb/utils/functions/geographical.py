import math
from numbers import Real
from decimal import Decimal
from typing import Optional
from .common import is_all_numeric, is_list_or_tuple, is_numeric
from ...types.types import (
    BoundingBoxDict,
    IncrementalBoundingBoxesDict,
    NumberOrNumbersList,
)


def get_bounding_box(
    latitude_in_degrees: Real = None,
    longitude_in_degrees: Real = None,
    half_side_in_km: Real = None,
) -> BoundingBoxDict:
    """
    Calculates a square boundingbox from any
    given geograhical center.

    half_side_in_km defines the size of the box.

    Return a BoundingBoxDict with keys:
    lat_min, lat_max, lng_min, lng_max.
    """
    if not all([latitude_in_degrees, longitude_in_degrees, half_side_in_km]):
        return None
    if half_side_in_km <= 0:
        return None
    if latitude_in_degrees < -90.0 or latitude_in_degrees > 90.0:
        return None
    if longitude_in_degrees < -180.0 or longitude_in_degrees > 180.0:
        return None

    lat = math.radians(latitude_in_degrees)
    lng = math.radians(longitude_in_degrees)

    earth_radius = 6371
    # Radius of the parallel at given latitude
    parallel_radius = earth_radius * math.cos(lat)

    lat_min = lat - half_side_in_km / earth_radius
    lat_max = lat + half_side_in_km / earth_radius
    lng_min = lng - half_side_in_km / parallel_radius
    lng_max = lng + half_side_in_km / parallel_radius
    rad2deg = math.degrees

    box = {
        "lat_min": Decimal(rad2deg(lat_min)),
        "lat_max": Decimal(rad2deg(lat_max)),
        "lng_min": Decimal(rad2deg(lng_min)),
        "lng_max": Decimal(rad2deg(lng_max)),
    }

    return box


def get_boundingboxes_incremental_steps(
    lat: Real,
    lng: Real,
    steps_m: Optional[NumberOrNumbersList] = None,
    exclude_prev_step_inner: bool = True,
) -> IncrementalBoundingBoxesDict:
    """
    Returns a dictionary of square boundingboxes
    in meter-incremented steps. Sorted from
    smallest to largest boundingbox.
    """
    if not is_all_numeric([lat, lng]):
        return None

    (lat, lng) = (float(lat), float(lng))

    if steps_m is None:
        steps_m = [100, 250, 500, 1000, 2500]
    else:
        if not is_list_or_tuple(steps_m):
            if is_numeric(steps_m):
                km = steps_m / 1000
                bbox: BoundingBoxDict = get_bounding_box(lat, lng, km)
                key = str(steps_m)
                return {key: {"boundingbox": bbox}}
            return None

        if not is_all_numeric(steps_m):
            return None

        steps_m = sorted(steps_m)

    boundingboxes = {}

    for i, m in enumerate(steps_m):
        key = str(m)
        km = m / 1000

        boundingboxes[key] = {
            "boundingbox": get_bounding_box(lat, lng, km),
        }

        if exclude_prev_step_inner and i > 0:
            prev_key = str(steps_m[(i - 1)])
            prev_bbox = boundingboxes[prev_key]["boundingbox"]
            boundingboxes[key]["exclude_inner"] = prev_bbox

    return boundingboxes
