from typeguard import check_type
from operator import itemgetter
from django.db.models.expressions import F
from django.db.models import Q
from geopy import distance
from ...models.geotags import GmapsGpsPoint
from ...models.local import LocalFile
from ...models.videoitem import Videoitem
from .geographical import get_boundingboxes_incremental_steps
from .common import get_parent_dir
from ...types.types import NumberOrNumbersList


def get_nearby_videoitems(
    videoitem: Videoitem,
    meters: NumberOrNumbersList = None,
    max_per_point: int = 10,
    max_per_group: int = 10,
    measure_precise: int = 2,
) -> dict:
    """
    Searches for Videoitems in close geographical distance
    to a given Videoitem, through GpsPoint reverse relations.

    Parameters:
    * meters: stepwise incremented boundingbox sizes,
    is also used for grouping results.
    * max_per_location: maximum Videoitems returned from each GpsPoint.
    * measure_precise: steps with precice measured distances
    (from steps-beginning).
    Any step after will have approximated distances. This will be
    reflected in the returned dictionary.
    Example: 12.34 versus <15.
    To speed up performance, cut down on precise measurements.
    """

    if videoitem is None or videoitem.gmaps_gps_point is None:
        return None
    if meters is None:
        meters = [120, 280, 550, 1100]
    else:
        check_type("NumberOrNumbersList", meters, NumberOrNumbersList)
        meters = sorted(meters)
        if not isinstance(meters, list):
            meters = [
                meters,
            ]

    ref_point = (videoitem.gps_lat, videoitem.gps_lng)

    nearby_items = {}

    boundingboxes = get_boundingboxes_incremental_steps(
        lat=float(videoitem.gps_lat),
        lng=float(videoitem.gps_lng),
        steps_m=meters,
        exclude_prev_step_inner=True,
    )

    outer_bounds_key = str(meters[-1])

    outer_bounds_filter = (
        Q(lat__lt=boundingboxes[outer_bounds_key]["boundingbox"]["lat_min"])
        | Q(lat__gt=boundingboxes[outer_bounds_key]["boundingbox"]["lat_max"])
        | Q(lng__lt=boundingboxes[outer_bounds_key]["boundingbox"]["lng_min"])
        | Q(lng__gt=boundingboxes[outer_bounds_key]["boundingbox"]["lng_max"])
    )

    outer_bounds_qs = GmapsGpsPoint.objects.exclude(outer_bounds_filter)
    for i, meter in enumerate(meters):
        precise = i < measure_precise
        key = str(meter)
        bbox = boundingboxes[key]["boundingbox"]
        (lat_min, lat_max, lng_min, lng_max) = itemgetter(
            "lat_min", "lat_max", "lng_min", "lng_max"
        )(bbox)
        outer_exclude = (
            Q(lat__lt=lat_min)
            | Q(lat__gt=lat_max)
            | Q(lng__lt=lng_min)
            | Q(lng__gt=lng_max)
        )
        inner_include = (
            Q(lat__gt=lat_min)
            & Q(lat__lt=lat_max)
            & Q(lng__gt=lng_min)
            & Q(lng__lt=lng_max)
        )
        if i == 0:
            qs = GmapsGpsPoint.objects.exclude(outer_exclude).filter(inner_include)
        else:
            prev_key = str(meters[i - 1])
            prev_bbox = boundingboxes[prev_key]["boundingbox"]
            (lat_min_prev, lat_max_prev, lng_min_prev, lng_max_prev) = itemgetter(
                "lat_min", "lat_max", "lng_min", "lng_max"
            )(prev_bbox)
            inner_exclude = (
                Q(lat__gt=lat_min_prev)
                & Q(lat__lt=lat_max_prev)
                & Q(lng__gt=lng_min_prev)
                & Q(lng__lt=lng_max_prev)
            )
        if i == len(meters) - 1:
            qs = outer_bounds_qs.exclude(inner_exclude)
        elif len(meters) - 1 > i > 0:
            qs = (
                GmapsGpsPoint.objects.exclude(outer_exclude)
                .exclude(inner_exclude)
                .filter(inner_include)
            )

        distances = []
        for gps_point in qs[:max_per_group]:
            point = (gps_point.lat, gps_point.lng)
            videoitems = gps_point.videoitems.all().values_list(
                "pk", "static_thumbnail_count"
            )[:max_per_point]
            distance_from_ref = (
                int(distance.distance(ref_point, point).meters)
                if precise
                else f"<{key}"
            )
            distances.append(
                {
                    "gps_point_id": gps_point.id,
                    "lat": gps_point.lat,
                    "lng": gps_point.lng,
                    "distance": distance_from_ref,
                    "videoitems": videoitems,
                }
            )
        if precise:
            distances = sorted(distances, key=lambda x: x["distance"])

        nearby_items[key] = distances

    return nearby_items


# scrap
def get_geotag_suggestions_from_local_dir(directory) -> list:
    qs = (
        LocalFile.objects.filter(directory_id__path__istartswith=directory)
        .exclude(videoitem_id_id__geotag_old__isnull=True)
        .annotate(
            geotag_old_id=F("videoitem_id__geotag_old_id__geotag_old_id"),
            location_displayname_short=F(
                "videoitem_id__geotag_old_id__location_displayname_short"
            ),
            directory_path=F("directory_id__path"),
        )
        .values(
            "geotag_old_id",
            "location_displayname_short",
            "directory_path",
        )
        .distinct()
    )

    results = list(qs)
    if results and isinstance(results, list):
        return results
    if results and isinstance(results, dict):
        return [
            results,
        ]
    return None


# scrap
def get_geotag_suggestions_from_local_dirs_recursive(directories):
    if isinstance(directories, str):
        directories = [
            directories,
        ]
    if not isinstance(directories, list):
        return None
    for dir in directories:
        geotag_suggestions = get_geotag_suggestions_from_local_dir(dir)
        if geotag_suggestions:
            return geotag_suggestions
        parent_dir = get_parent_dir(dir)
        geotag_suggestions = get_geotag_suggestions_from_local_dir(parent_dir)
        if geotag_suggestions:
            return geotag_suggestions
        return get_geotag_suggestions_from_local_dirs_recursive(parent_dir)


def get_directory_items(directory):
    qs = LocalFile.objects.filter(directory_id__path__istartswith=directory)
    return [x.videoitem_id for x in qs]
