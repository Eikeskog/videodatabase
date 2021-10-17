import json
from numbers import Real
from typing import Optional, Type, TypeVar, Union
from django.db import models
from django.db.models.base import Model
from django.db.models.query import QuerySet
from django.utils.module_loading import import_string
from django.forms.models import model_to_dict
from time import sleep
from timeit import default_timer as timer
from geopy import distance
from typeguard import check_type
from ..types.types import (
    BoundingBoxDict,
    GeocodeDict,
    LatLngTuple,
    MultiLevelGeocodeDict,
)
from ..utils.functions.geographical import get_bounding_box
from ..utils.functions.geocoding import get_reverse_geotags_gmaps


SORTED_ADDRESS_FIELDS = [
    "locality",
    "postal_town",
    "postal_code",
    "municipality",
    "county",
    "country_code",
]

T = TypeVar("T", bound=Model)


class ScheduledReverseGeotag(models.Model):
    gps_point = models.ForeignKey(
        to="GmapsGpsPoint",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="scheduled_reverse_geotag",
    )

    geotag_lvl_1 = models.ForeignKey(
        to="GeotagLvl1",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="scheduled_reverse_geotag",
    )

    lat = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)
    lng = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)

    class Meta:
        db_table = "scheduled_reverse_geotag"

    @classmethod
    def gps_point_is_scheduled(cls, gps_point: object) -> bool:
        """Checks if a gps_point is already scheduled for reverse geocode"""
        return cls.objects.filter(gps_point=gps_point).exists()

    @classmethod
    def schedule_if_not_scheduled(cls, gps_point: object) -> None:
        """
        Checks if a GpsPoint is scheduled for reverse geocode,
        schedules new if not.
        """
        if not cls.gps_point_is_scheduled(gps_point):
            cls.objects.create(
                gps_point=gps_point, lat=gps_point.lat, lng=gps_point.lng
            )

    @classmethod
    def get_gmaps_geotag_dict(cls, latlng: LatLngTuple) -> MultiLevelGeocodeDict:
        """Execute reverse geocoding"""
        geocode_dict = get_reverse_geotags_gmaps(latlng)
        return geocode_dict

    @classmethod
    def clear_complete(cls) -> None:
        cls.objects.filter(geotag_lvl_1_id__isnull=False).delete()

    @classmethod
    def run_batch_reverse(cls) -> None:
        def throttle(time_start, time_end, condition=True):
            max_throttle = 0.05
            if not condition or (max_throttle - time_end - time_start) < 0:
                return
            return sleep((max_throttle - time_end - time_start))

        new_geotags = []
        qs = cls.objects.all()
        qs_len = qs.count()

        for scheduled in qs:
            geotag = None
            for new_geotag in new_geotags:
                if all(
                    [
                        new_geotag.lat_min < scheduled.lat,
                        new_geotag.lat_max > scheduled.lat,
                        new_geotag.lng_min < scheduled.lng,
                        new_geotag.lng_max > scheduled.lng,
                        new_geotag.areal < 100,
                    ]
                ):
                    geotag = new_geotag
                    break

            if not geotag:
                time_start = timer()
                latlng = (
                    scheduled.lat,
                    scheduled.lng,
                )
                geotag_dict = cls.get_gmaps_geotag_dict(latlng)
                if not geotag_dict:
                    continue
                geotag = GeotagLvl1._new_from_geocode_dict(geotag_dict)
                if geotag:
                    new_geotags.append(geotag)
                    new_geotags.sort(key=lambda obj: obj.areal)
                else:
                    continue

            scheduled.geotag_lvl_1 = geotag
            scheduled.save()

            gps_point = scheduled.gps_point
            gps_point.geotag_lvl_1 = geotag

            gps_point.save()

            time_end = timer()
            throttle(time_start, time_end, condition=(qs_len >= 50))

        cls.clear_complete()


class Geotag(models.Model):
    lat_min = models.DecimalField(
        max_digits=11, decimal_places=7, null=True, blank=True
    )
    lat_max = models.DecimalField(
        max_digits=11, decimal_places=7, null=True, blank=True
    )
    lng_min = models.DecimalField(
        max_digits=11, decimal_places=7, null=True, blank=True
    )
    lng_max = models.DecimalField(
        max_digits=11, decimal_places=7, null=True, blank=True
    )

    unique_displayname_object = models.ForeignKey(
        to="UniqueLocationDisplayname",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="geotag_set",
    )

    parent = models.ForeignKey(
        to="self", null=True, blank=True, on_delete=models.SET_NULL
    )

    distances = models.JSONField(null=True, blank=True)
    areal = models.FloatField(null=True, blank=True)

    plus_code = models.CharField(max_length=120, default="", blank=True)

    locality = models.CharField(max_length=120, default="", blank=True)
    postal_town = models.CharField(max_length=120, default="", blank=True)
    postal_code = models.IntegerField(null=True, blank=True)
    municipality = models.CharField(max_length=120, default="", blank=True)
    county = models.CharField(max_length=120, default="", blank=True)
    country_code = models.CharField(max_length=2, default="", blank=True)

    formatted_address = models.CharField(max_length=255, default="", blank=True)
    other_fields = models.JSONField(null=True, blank=True)

    displayname_short = models.CharField(max_length=255, default="", blank=True)
    displayname_full = models.CharField(max_length=255, default="", blank=True)

    def is_plus_code(self) -> bool:
        return self.plus_code is not None

    def get_plus_code(self) -> str:
        return self.plus_code

    def has_other_fields(self) -> bool:
        return self.other_fields is not None

    def get_other_fields(self) -> Optional[dict]:
        if not self.has_other_fields():
            return None
        return json.loads(self.other_fields)

    def contains_latlng(self, latlng: LatLngTuple) -> bool:
        (lat, lng) = latlng
        return all(
            [(self.lat_min < lat < self.lat_max), (self.lng_min < lng < self.lng_max)]
        )

    @classmethod
    def get_smallest_container(
        cls: Type[T],
        latlng: LatLngTuple,
    ) -> Optional[T]:
        """
        If exists, return Geotag instance with smallest
        square area boundingbox, where a given LatLngTuple will fit.
        """
        (lat, lng) = latlng
        qs = Geotag.objects.filter(
            lat_min__lt=lat,
            lat_max__gt=lat,
            lng_min__lt=lng,
            lng_max__gt=lng,
        ).order_by("areal")
        print(f"qs: {qs}")
        return qs[0] if qs else None

    @classmethod
    def _extract_geocode_dict_bbox(cls, geocode_dict: GeocodeDict):
        """Extracts boundingbox from a GeocodeDict."""
        return {
            "lat_min": geocode_dict["lat_min"],
            "lat_max": geocode_dict["lat_max"],
            "lng_min": geocode_dict["lng_min"],
            "lng_max": geocode_dict["lng_max"],
        }

    def _update_from_dict(
        self, geocode_dict: GeocodeDict, exclude_keys: Optional[list[Union[str, int]]]
    ) -> None:
        """Update a Geotag instance from a GeocodeDict."""
        other_fields = {}
        if self.other_fields is not None:
            other_fields = json.loads(self.other_fields)
        for key, value in geocode_dict.items():
            if exclude_keys and key in exclude_keys:
                continue
            if hasattr(self, key) and value not in [None, "", " "]:
                setattr(self, key, value)
            else:
                other_fields[key] = value
        if len(other_fields.keys()):
            self.other_fields = json.dumps(other_fields)
        self.save()

    def _calc_bbox_areal(self) -> None:
        """
        Calculates and sets boundingbox areal
        in an existing Geotag instance.
        """
        if self.areal is not None:
            return
        if "ns" not in self.distances or "ew" not in self.distances:
            return
        self.areal = self.distances["ns"] * self.distances["ew"]
        self.save()

    def bbox_areal(self) -> float:  # Decimal?
        """Return boundingbox areal in square meters."""
        if self.areal is None:
            self._calc_bbox_areal()
        return self.areal

    def get_gps_points(self, limit: int) -> Optional[QuerySet]:
        return self.gps_points.all()[:limit]

    def get_videoitems(self, limit: int = 10) -> Optional[list[Optional[QuerySet]]]:
        """
        Look up reverse foreign relations through GpsPoint.
        Return a list of Videoitem QuerySets.
        """
        if self.level != 1:
            return None
        gps_points: QuerySet = self.get_gps_points(limit)
        querysets = [gps_point.get_videoitems(limit) for gps_point in gps_points]
        return querysets

    def get_displayname_short_values(self) -> str:
        """
        Convert displayname positions to field values.
        """
        fields = self.displayname_short.split(",")
        model_dict = model_to_dict(self, fields=fields)
        displayname = ", ".join(
            model_dict[x] for x in fields if all([x is not None, model_dict[x]])
        ).replace("fylke", "")

        return displayname.strip()

    @classmethod
    def _new_from_geocode_dict(cls: Type[T], geocode_dict: MultiLevelGeocodeDict) -> T:
        """
        Creates a new chain of connected Geotags (levels 1 through 5)
        from a MultiLevelGeocodeDict. (Connects each with preceding parent).

        Return the first object in the chain (GeotagLvl1).
        """
        if not isinstance(geocode_dict, dict):
            raise AssertionError(
                "Parameter 'gmaps_reverse_geocoding_dict' must be a dictionary"
            )
        levels = len(geocode_dict.keys())
        if levels == 0:
            raise AssertionError("Empty dictionary: gmaps_reverse_geocoding_dict")
        if levels > 5:
            raise AssertionError(
                "len(gmaps_reverse_geocoding_dict.keys()) must not exceed 5"
            )

        lvl_1 = None
        prev_geotag = None
        for lvl in range(1, (levels + 1)):
            key = f"level_{lvl}"
            if key not in geocode_dict:
                raise AssertionError(
                    "gmaps_reverse_geocoding_dict keys must be in str format: 'level_<int>'"
                )
            cur_dict: GeocodeDict = geocode_dict[key]
            cur_bbox: BoundingBoxDict = cls._extract_geocode_dict_bbox(cur_dict)
            cur_class = cls.__get_class(lvl)

            (obj, created) = cur_class.objects.get_or_create(**cur_bbox)

            if lvl == 1:
                lvl_1 = obj

            if created:
                exclude_keys = list(cur_bbox.keys())
                obj._update_from_dict(cur_dict, exclude_keys=exclude_keys)
                obj._calc_bbox_areal()

            if prev_geotag is None:
                prev_geotag = obj
                continue

            if prev_geotag.parent is None:
                prev_geotag.parent = obj

            prev_geotag.save()
            prev_geotag = obj

        return lvl_1

    @classmethod
    def __get_class(cls, lvl=0):
        if 0 > lvl > 5:
            raise AssertionError(f"geotag level {lvl} doesn't exist")
        _cls = import_string(f"videodb.models.geotags.GeotagLvl{lvl}")
        return _cls

    def get_parent_class(self):
        if self.level == 5:
            return None
        return Geotag.__get_class(self.level + 1)

    def get_child_class(self):
        if self.level == 0:
            return None
        return Geotag.__get_class(self.level - 1)

    def get_address_dict(self):
        address_dict = {
            k: v
            for k, v in model_to_dict(self).items()
            if v and k in SORTED_ADDRESS_FIELDS
        }
        return address_dict


class GeotagLvl1(Geotag):
    level = 1

    class Meta:
        db_table = "geotag_lvl_1"


class GeotagLvl2(Geotag):
    level = 2

    class Meta:
        db_table = "geotag_lvl_2"


class GeotagLvl3(Geotag):
    level = 3

    class Meta:
        db_table = "geotag_lvl_3"


class GeotagLvl4(Geotag):
    level = 4

    class Meta:
        db_table = "geotag_lvl_4"


class GeotagLvl5(Geotag):
    level = 5

    class Meta:
        db_table = "geotag_lvl_5"


class GmapsGpsPoint(models.Model):
    lat = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)
    lng = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)

    geotag_lvl_1 = models.ForeignKey(
        to="Geotag",
        on_delete=models.CASCADE,
        related_name="gps_points",
        null=True,
        blank=True,
    )

    custom_displayname = models.CharField(max_length=120, default="", blank=True)

    class Meta:
        db_table = "gmaps_gpspoint"

    def get_videoitems(self, limit: int) -> QuerySet:
        return self.videoitems.all()[:limit]

    def get_displayname_short(self) -> str:
        if self.custom_displayname not in [None, "", " "]:
            return self.custom_displayname
        if self.geotag_lvl_1:
            return self.geotag_lvl_1.get_displayname_short_values()

    def _distance_to_point(self, latlng):
        return distance.distance(
            (
                self.lat,
                self.lng,
            ),
            latlng,
        )

    @classmethod
    def _snap_to_existing(
        cls: Type[T],
        latlng: LatLngTuple,
        m_max: Real = 2,
    ) -> Optional[T]:
        """
        Looks up a LatLngTuple and searches for
        an existing GpsPoint within in a specified
        range in meters.
        """
        bbox = get_bounding_box(latlng[0], latlng[1], (1000 / m_max))
        qs = GmapsGpsPoint.objects.filter(
            lat__gt=bbox["lat_min"],
            lat__lt=bbox["lat_max"],
            lng__gt=bbox["lng_min"],
            lng__lt=bbox["lng_max"],
        )
        if not qs:
            return None
        for obj in qs:
            if obj._distance_to_point(latlng).meters <= 1:
                return obj
        return None

    @classmethod
    def _get_approx_or_create_new(
        cls: Type[T], latlng: LatLngTuple, m_max: Real = 2
    ) -> T:
        """
        Looks up a LatLngTuple and searches for
        an existing GpsPoint within in a specified
        range in meters.
        Creates a new instance if not found.

        Return GpsPoint.
        """
        obj = cls._snap_to_existing(latlng, m_max)
        if not obj:
            obj = GmapsGpsPoint.objects.create(lat=latlng[0], lng=latlng[1])
        return obj

    def _connect_with_geotag(self) -> object:
        if self.geotag_lvl_1 is not None:
            return self
        geotag = Geotag.get_smallest_container(latlng=(self.lat, self.lng))
        if not geotag:
            ScheduledReverseGeotag.schedule_if_not_scheduled(self)
        else:
            self.geotag_lvl_1 = geotag
            self.save()
        return self

    @classmethod
    def get_by_latlng(cls: Type[T], latlng: LatLngTuple) -> T:
        # check_type("LatLngTuple", latlng, LatLngTuple)
        obj = cls._get_approx_or_create_new(latlng, m_max=2)
        obj._connect_with_geotag()
        return obj
