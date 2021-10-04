import datetime
import django_filters
from django.utils.timezone import make_aware
from django.db.models import Q
from .models.videoitem import Videoitem
from .models.local import LocalFile
from .models.keyword import Keyword
from .models.unique_searchfilter import (
    UniqueCamera,
    UniqueLocationDisplayname,
    UniqueFps
)
from .models.geotags import (
    GeotagLevel1,
    GeotagLevel2,
    GeotagLevel3,
    GeotagLevel4,
    GeotagLevel5
)

class LocationFilter(django_filters.FilterSet):
    s = django_filters.CharFilter(method="displayname_filter")

    def displayname_filter(self, queryset, name, value):
        ids = queryset.filter(most_specific_field_value__istartswith = value)
        if len(ids) == 0:
            ids_names = UniqueLocationDisplayname.get_unique_displaynames_any_address_field_startswith(value)
            if ids_names:
                second_ids = [key for key in ids_names.keys()]
                ids = queryset.filter(id__in=second_ids)[:10]

        return ids

class VideoitemsFilter(django_filters.FilterSet):
    exif_fps__in = django_filters.CharFilter(method="fps_filter")
    exif_camera__in = django_filters.CharFilter(method="camera_filter")
    location_displayname__in = django_filters.CharFilter(method="location_displayname_filter")
    daterange__in = django_filters.CharFilter(method="daterange_filter")
    keyword__in = django_filters.CharFilter(method="keyword_filter")
    project__in = django_filters.CharFilter(method="project_filter")

    def daterange_filter(self, queryset, name, value):
        query = Q()
        
        for daterange in value.split(","):
            (start, end) = daterange.split('_')
            
            date_start = make_aware(datetime.datetime.strptime(
                start + ' 00:00:01', '%Y-%m-%d %H:%M:%S'))
            date_end = make_aware(datetime.datetime.strptime(
                end + ' 23:59:59', '%Y-%m-%d %H:%M:%S'))

            query |= Q(
                exif_last_modified__gt = date_start,
                exif_last_modified__lt = date_end,
            )

        return queryset.filter(query)

    def camera_filter(self, queryset, name, value):
        ids = value.split(",")
        labels = UniqueCamera.objects.filter(
            id__in=ids
        ).values_list('camera', flat=True)
        
        return queryset.filter(exif_camera__in=labels)

    def fps_filter(self, queryset, name, value):
        ids = value.split(",")
        labels = UniqueFps.objects.filter(
            id__in=ids
        ).values_list('fps', flat=True)

        return queryset.filter(exif_fps__in=labels)

    def keyword_filter(self, queryset, name, value, filter_method='AND'):
        first_filtering = []

        for keyword in value.split(","):
            first_filtering.append(Keyword.objects.filter(
                unique_keyword = keyword
            ).select_related('videoitem').values_list('videoitem_id', flat=True))

        if filter_method == 'AND':
            return queryset.filter(
                videoitem_id__in = list(set(first_filtering[0]).intersection(*first_filtering))
            )
            
        return queryset.filter(videoitem_id__in = first_filtering)

    def project_filter(self, queryset, name, value):
        return queryset.filter(
            pk__in = LocalFile.objects.filter(
                directory_id__project_roll_directory_id__project_main_directory_id__project_id__project_id__in = value.split(",")
            ).values_list('videoitem', flat=True))

    # rewrite
    def location_displayname_filter(self, queryset, name, value):
        ids = value.split(",")

        geotags_query = Q()

        for obj in UniqueLocationDisplayname.objects.filter(id__in = ids):
            not_null_fields = obj.get_unique_address_fields_not_null()

            geotags_query |= Q(
                **not_null_fields
            ) | Q(
                unique_displayname_object_id__in = ids
            )

        geotag_classes = [GeotagLevel1, GeotagLevel2, GeotagLevel3, GeotagLevel4, GeotagLevel5]
        
        geotags_qs = [geotag_class.objects.filter(geotags_query) for geotag_class in geotag_classes]

        query = Q(
            gmaps_gps_point_id__geotag_level_1_id__in = geotags_qs[0],
        ) | Q(
            gmaps_gps_point_id__geotag_level_1_id__geotag_level_2_id__in = geotags_qs[1],
        ) | Q(
            gmaps_gps_point_id__geotag_level_1_id__geotag_level_2_id__geotag_level_3_id__in = geotags_qs[2],
        ) | Q(
            gmaps_gps_point_id__geotag_level_1_id__geotag_level_2_id__geotag_level_3_id__geotag_level_4_id__in = geotags_qs[3],
        ) | Q(
            gmaps_gps_point_id__geotag_level_1_id__geotag_level_2_id__geotag_level_3_id__geotag_level_4_id__geotag_level_5_id__in = geotags_qs[4],
        )

        return queryset.exclude(gmaps_gps_point__isnull=True).filter(query)