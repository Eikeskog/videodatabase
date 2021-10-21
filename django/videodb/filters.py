import datetime
import django_filters
from django.utils.timezone import make_aware
from django.db.models import Q
from .models.local import LocalFile
from .models.keyword import Keyword
from .models.unique_searchfilter import (
    UniqueCamera,
    UniqueLocationDisplayname,
    UniqueFps,
)
from .models.geotags import (
    GeotagLvl1,
    GeotagLvl2,
    GeotagLvl3,
    GeotagLvl4,
    GeotagLvl5,
)

GEOTAG_CLASSES = [
    GeotagLvl1,
    GeotagLvl2,
    GeotagLvl3,
    GeotagLvl4,
    GeotagLvl5,
]


class LocationFilter(django_filters.FilterSet):
    s = django_filters.CharFilter(method="displayname_filter")

    def displayname_filter(self, queryset, name, value):
        qs = UniqueLocationDisplayname.objects.filter(
            most_specific_field_value__istartswith=value
        )
        qs_len = qs.count()
        if qs_len < 10:
            limit = 10 - qs_len
            ids_values = UniqueLocationDisplayname.any_field_startswith(
                str_startswith=value, limit=limit
            )
            if ids_values:
                new_qs = UniqueLocationDisplayname.objects.exclude(id__in=qs).filter(
                    id__in=list(ids_values.keys())
                )[:limit]
                qs = qs.union(new_qs)
                for x in qs:
                    if str(x.id) in ids_values:
                        x.temp_label = ids_values[str(x.id)]
        return qs


class VideoitemsFilter(django_filters.FilterSet):
    exif_fps__in = django_filters.CharFilter(method="fps_filter")
    exif_camera__in = django_filters.CharFilter(method="camera_filter")
    location_displayname__in = django_filters.CharFilter(
        method="location_displayname_filter"
    )
    daterange__in = django_filters.CharFilter(method="daterange_filter")
    keyword__in = django_filters.CharFilter(method="keyword_filter")
    project__in = django_filters.CharFilter(method="project_filter")

    def location_displayname_filter(self, queryset, name, value):
        ids = value.split(",")

        geotags_query = Q()

        for obj in UniqueLocationDisplayname.objects.filter(id__in=ids):
            not_null_fields = obj.get_unique_address_fields_not_null()
            geotags_query |= Q(**not_null_fields) | Q(
                unique_displayname_object_id__in=ids
            )

        geotags_qs = [
            geotag_class.objects.filter(geotags_query)
            for geotag_class in GEOTAG_CLASSES
        ]

        level_1 = "gmaps_gps_point_id__geotag_lvl_1_id"
        level_2 = f"{level_1}__parent_id"
        level_3 = f"{level_2}__parent_id"
        level_4 = f"{level_3}__parent_id"
        level_5 = f"{level_4}__parent_id"
        query = (
            Q(**{f"{level_1}__in": geotags_qs[0]})
            | Q(**{f"{level_2}__in": geotags_qs[1]})
            | Q(**{f"{level_3}__in": geotags_qs[2]})
            | Q(**{f"{level_4}__in": geotags_qs[3]})
            | Q(**{f"{level_5}__in": geotags_qs[4]})
        )

        return queryset.exclude(gmaps_gps_point__isnull=True).filter(query)

    def daterange_filter(self, queryset, name, value):
        query = Q()

        for daterange in value.split(","):
            (start, end) = daterange.split("_")

            date_start = make_aware(
                datetime.datetime.strptime(start + " 00:00:01", "%Y-%m-%d %H:%M:%S")
            )
            date_end = make_aware(
                datetime.datetime.strptime(end + " 23:59:59", "%Y-%m-%d %H:%M:%S")
            )

            query |= Q(
                exif_last_modified__gt=date_start,
                exif_last_modified__lt=date_end,
            )

        return queryset.filter(query)

    def camera_filter(self, queryset, name, value):
        ids = value.split(",")
        labels = UniqueCamera.objects.filter(id__in=ids).values_list(
            "camera", flat=True
        )

        return queryset.filter(exif_camera__in=labels)

    def fps_filter(self, queryset, name, value):
        ids = value.split(",")
        labels = UniqueFps.objects.filter(id__in=ids).values_list("fps", flat=True)

        return queryset.filter(exif_fps__in=labels)

    def keyword_filter(self, queryset, name, value, filter_method="AND"):
        first_filtering = []

        for keyword in value.split(","):
            first_filtering.append(
                Keyword.objects.filter(unique_keyword=keyword)
                .select_related("videoitem")
                .values_list("videoitem_id", flat=True)
            )

        if filter_method == "AND":
            return queryset.filter(
                videoitem_id__in=list(
                    set(first_filtering[0]).intersection(*first_filtering)
                )
            )

        return queryset.filter(videoitem_id__in=first_filtering)

    def project_filter(self, queryset, name, value):
        reverse_lookup = (
            "directory_id__"
            "project_roll_directory_id__"
            "project_main_directory_id__"
            "project_id__pk__in"
        )
        return queryset.filter(
            pk__in=LocalFile.objects.filter(
                **{reverse_lookup: value.split(",")}
            ).values_list("videoitem", flat=True)
        )
