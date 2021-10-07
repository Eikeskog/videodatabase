from django.db.models.expressions import F
from django.db.models import Q
from geopy import distance
from ...models.geotags import GmapsGpsPoint
from ...models.local import LocalFile
from ...models.videoitem import Videoitem

# from .geographical import get_bounding_box
from .geographical import get_boundingboxes_incremental_steps
from .common import (
    is_all_numeric,
    is_list_or_tuple,
    is_numeric,
    get_parent_dir
)


def get_nearby_videoitems(
    videoitem,
    meters = None
):
    if meters is None:
        meters = [120, 280, 550, 1100]
    if not is_list_or_tuple(meters):
        if is_numeric(meters):
            meters = [meters,]
        else: 
          return None

    if not is_all_numeric(meters):
        return None

    nearby_points = {}
    meters = sorted(meters)

    boundingboxes = get_boundingboxes_incremental_steps(
        lat = float(videoitem.gps_lat),
        lng = float(videoitem.gps_lng),
        steps_m = meters,
        exclude_prev_step_inner = True
    )

    outer_bounds_key = str(meters[-1])

    outer_bounds_filter = Q(
        lat__lt = boundingboxes[outer_bounds_key]['boundingbox']['lat_min']
    ) | Q(
        lat__gt = boundingboxes[outer_bounds_key]['boundingbox']['lat_max']
    ) | Q(
        lng__lt = boundingboxes[outer_bounds_key]['boundingbox']['lng_min']
    ) | Q(
        lng__gt = boundingboxes[outer_bounds_key]['boundingbox']['lng_max']
    )

    outer_bounds_qs = GmapsGpsPoint.objects.exclude(outer_bounds_filter)

    for i, meter in enumerate(reversed(meters)):
        key = str(meter)
        if i == 0:
            prev_key = key
            qs = outer_bounds_qs
        else:
            qs = outer_bounds_qs.exclude(
                Q(
                    lat__lt = boundingboxes[prev_key]['boundingbox']['lat_min']
                ) | Q(
                    lat__gt = boundingboxes[prev_key]['boundingbox']['lat_max']
                ) | Q(
                    lng__lt = boundingboxes[prev_key]['boundingbox']['lng_min']
                ) | Q(
                    lng__gt = boundingboxes[prev_key]['boundingbox']['lng_max']
                )
            )

        if i < len(meters)-1:
            inner_bounds_exclude = Q(
                lat__gt = boundingboxes[key]['exclude_inner']['lat_min']
            ) & Q(
                lat__lt = boundingboxes[key]['exclude_inner']['lat_max']
            ) & Q(
                lng__gt = boundingboxes[key]['exclude_inner']['lng_min']
            ) & Q(
                lng__lt = boundingboxes[key]['exclude_inner']['lng_max']
            )

            qs = qs.exclude(inner_bounds_exclude)

        if i > 0:
            inner_bounds_include = Q(
                lat__gt = boundingboxes[key]['boundingbox']['lat_min']
            ) & Q(
                lat__lt = boundingboxes[key]['boundingbox']['lat_max']
            ) & Q(
                lng__gt = boundingboxes[key]['boundingbox']['lng_min']
            ) & Q(
                lng__lt = boundingboxes[key]['boundingbox']['lng_max']
            )
            qs = qs.filter(inner_bounds_include)

        if key in [str(x) for x in meters[:2]]:
            distances = []

            for gps_point_obj in qs:
                point1 = (videoitem.gps_lat, videoitem.gps_lng,)
                point2 = (gps_point_obj.lat, gps_point_obj.lng,)
                points_distance = distance.distance(point1, point2)
                distances.append(
                    {
                        'gps_point_id': gps_point_obj.id,
                        'lat': gps_point_obj.lat,
                        'lng': gps_point_obj.lng,
                        'distance': points_distance.meters,
                        'videoitems': [
                            obj.pk
                            for obj in Videoitem.objects
                                .exclude(gmaps_gps_point__isnull = True)
                                .filter(gmaps_gps_point_id = gps_point_obj.id)
                        ][:20]
                    }
                )

            nearby_points[key] = distances

        else:
            distances = []
            for gps_point_obj in qs:
                distances.append(
                    {
                        'gps_point_id': gps_point_obj.id,
                        'lat': gps_point_obj.lat,
                        'lng': gps_point_obj.lng,
                        'distance': f'< {key}',
                        'videoitems': [
                            obj.pk
                            for obj in Videoitem.objects
                                .exclude(gmaps_gps_point__isnull = True)
                                .filter(gmaps_gps_point_id = gps_point_obj.id)
                        ][:20]
                    }
                )
            nearby_points[key] = distances

        prev_key = key

    return nearby_points


# gammel funksjon, har nå en directory modell som heller kan brukes
def get_geotag_suggestions_from_local_dir(directory):
    qs = LocalFile.objects.filter(
                directory_id__path__istartswith=directory
            ).exclude(
                videoitem_id_id__geotag_old__isnull=True
            ).annotate(
                geotag_old_id = F('videoitem_id__geotag_old_id__geotag_old_id'),
                location_displayname_short = F('videoitem_id__geotag_old_id__location_displayname_short'),
                directory_path = F('directory_id__path')
            ).values(
                'geotag_old_id',
                'location_displayname_short',
                'directory_path',
            ).distinct()

    results = list(qs)
    if results and isinstance(results, list):
        return results
    if results and isinstance(results, dict):
        return [results,]
    return None


def get_geotag_suggestions_from_local_dirs_recursive(directories):
    if isinstance(directories, str): directories = [directories,]
    if not isinstance(directories, list): return None
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