from django.db import models
from django.utils.module_loading import import_string
from django.forms.models import model_to_dict
from time import sleep
from timeit import default_timer as timer
import geopy.distance
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


class ScheduledReverseGeotag(models.Model):
    gps_point = models.ForeignKey(
        to="GmapsGpsPoint",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="scheduled_reverse_geotag",
    )
    geotag_level_1 = models.ForeignKey(
        to="GeotagLevel1",
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
        return cls.objects.filter(gps_point=gps_point).exists()

    @classmethod
    def schedule_if_not_scheduled(cls, gps_point: object) -> None:
        if not cls.gps_point_is_scheduled(gps_point):
            cls.objects.create(
                gps_point=gps_point, lat=gps_point.lat, lng=gps_point.lng
            )

    @classmethod
    def get_gmaps_geotag_dict(cls, latlng: tuple) -> dict:
        return get_reverse_geotags_gmaps(latlng)

    @classmethod
    def clear_complete(cls) -> None:
        cls.objects.filter(geotag_level_1_id__isnull=False).delete()
        cls.objects.filter(geotag_lvl_1_id__isnull=False).delete()
        return

    @classmethod
    def run_batch_reverse(cls) -> None:
        def throttle(time_start, time_end, condition=True):
            max_throttle = 0.05
            if not condition or (max_throttle - time_end - time_start) < 0:
                return
            return sleep((max_throttle - time_end - time_start))

        new_geotags = []
        new_geotags2 = []

        qs = cls.objects.all()
        qs_len = len(qs)

        for scheduled in qs:
            geotag = None
            for new_geotag in new_geotags:
                if all(
                    [
                        new_geotag.lat_min < scheduled.lat,
                        new_geotag.lat_max > scheduled.lat,
                        new_geotag.lng_min < scheduled.lng,
                        new_geotag.lng_max > scheduled.lng,
                    ]
                ):
                    geotag = new_geotag
                    break

            if not geotag:
                time_start = timer()
                geotag_dict = cls.get_gmaps_geotag_dict(
                    (
                        scheduled.lat,
                        scheduled.lng,
                    )
                )
                if not geotag_dict:
                    continue
                geotag = GeotagLevel1.new_from_dict(geotag_dict)
                geotag2 = GeotagLvl1.new_from_dict(geotag_dict)
                if geotag:
                    new_geotags.append(geotag)
                    new_geotags2.append(geotag2)
                else:
                    continue

            scheduled.geotag_level_1 = geotag
            scheduled.geotag_lvl_1 = geotag2
            scheduled.save()

            gps_point = scheduled.gps_point
            gps_point.geotag_level_1 = geotag
            gps_point.geotag_lvl_1 = geotag2

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

    distances = models.JSONField(null=True, blank=True)
    areal = models.FloatField(null=True, blank=True)

    locality = models.CharField(max_length=120, default="", blank=True)
    postal_town = models.CharField(max_length=120, default="", blank=True)
    postal_code = models.IntegerField(null=True, blank=True)
    municipality = models.CharField(max_length=120, default="", blank=True)
    county = models.CharField(max_length=120, default="", blank=True)
    country_code = models.CharField(max_length=2, default="", blank=True)

    displayname_short = models.CharField(max_length=255, default="", blank=True)
    displayname_full = models.CharField(max_length=255, default="", blank=True)

    def contains_point(self, point):
        (lat, lng) = point
        return all(
            [(self.lat_min < lat < self.lat_max), (self.lng_min < lng < self.lng_max)]
        )

    @classmethod
    def get_smallest_containing(cls, point):
        (lat, lng) = point
        qs = GeotagLvl1.objects.filter(
            lat_min__lt=lat,
            lat_max__gt=lat,
            lng_min__lt=lng,
            lng_max__gt=lng,
        ).order_by('areal')[0]
        return qs

    @classmethod
    def _geocode_dict_bbox(geocode_dict):
        return {
            "lat_min": geocode_dict["lat_min"],
            "lat_max": geocode_dict["lat_max"],
            "lng_min": geocode_dict["lng_min"],
            "lng_max": geocode_dict["lng_max"],
        }

    def _update_from_dict(self, dictionary, exclude_keys):
        for key, value in dictionary.items():
            if exclude_keys and key in exclude_keys:
                continue
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def bbox_areal(self) -> float:
        if not self.areal:
            self.areal = self.distances["ns"] * self.distances["ew"]
            self.save()
        return self.areal

    def get_videoitems(self, limit: int):
        if self.level != 1:
            return
        return [x.get_videoitems(limit) for x in self.gps_points.all()[:limit]]

    def get_displayname_short(self) -> str:
        fields = self.displayname_short.split(",")
        model_dict = model_to_dict(self, fields=fields)

        displayname = ", ".join(
            model_dict[x] for x in fields if all([x is not None, model_dict[x]])
        ).replace("fylke", "")

        return displayname.strip()

    @classmethod
    def new_from_geocode_dict(cls, gmaps_geocode_dict, levels=5):
        if not isinstance(levels, int) or 1 > levels > 5:
            raise AssertionError("levels must be a number from 1 to 5.")
        if not isinstance(gmaps_geocode_dict, dict):
            raise AssertionError("gmaps_reverse_geocoding_dict must be a dictionary")

        prev_geotag = None
        for lvl in range(1, levels):
            key = f"level_{lvl}"
            if key not in gmaps_geocode_dict:
                continue
            cur_dict = gmaps_geocode_dict[key]
            cur_bbox = cls._geocode_dict_bbox(cur_dict)
            cur_class = cls.__get_class(lvl)

            (obj, created) = cur_class.objects.get_or_create(**cur_bbox)

            if created:
                obj._update_from_dict(cur_dict, exclude_keys=list(cur_bbox.keys()))

            if prev_geotag is None:
                prev_geotag = obj
                continue

            if prev_geotag.parent is None:
                prev_geotag.parent = obj

            prev_geotag.save()
            prev_geotag = obj

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
    parent = models.ManyToManyField(to="GeotagLvl2", related_name="children")

    class Meta:
        db_table = "geotag_lvl_1"

    unique_displayname_object = models.ForeignKey(
        to="UniqueLocationDisplayname",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="geotag_lvl_1_set",
    )

    def say(self, arg):
        return Geotag.say(self, arg)


class GeotagLvl2(Geotag):
    level = 2
    parent = models.ManyToManyField(to="GeotagLvl3", related_name="children")
    unique_displayname_object = models.ForeignKey(
        to="UniqueLocationDisplayname",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="geotag_lvl_2_set",
    )

    class Meta:
        db_table = "geotag_lvl_2"


class GeotagLvl3(Geotag):
    level = 3
    parent = models.ManyToManyField(to="GeotagLvl4", related_name="children")
    unique_displayname_object = models.ForeignKey(
        to="UniqueLocationDisplayname",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="geotag_lvl_3_set",
    )

    class Meta:
        db_table = "geotag_lvl_3"


class GeotagLvl4(Geotag):
    level = 4
    parent = models.ManyToManyField(to="GeotagLvl5", related_name="chldren")
    unique_displayname_object = models.ForeignKey(
        to="UniqueLocationDisplayname",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="geotag_lvl_4_set",
    )

    class Meta:
        db_table = "geotag_lvl_4"


class GeotagLvl5(Geotag):
    level = 5
    parent = None

    unique_displayname_object = models.ForeignKey(
        to="UniqueLocationDisplayname",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="geotag_lvl_5_set",
    )

    class Meta:
        db_table = "geotag_lvl_5"


class GeotagLevel5(models.Model):
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

    displayname_short = models.CharField(max_length=255, default="", blank=True)
    displayname_full = models.CharField(max_length=255, default="", blank=True)

    postal_town = models.CharField(max_length=120, default="", blank=True)
    locality = models.CharField(max_length=120, default="", blank=True)
    county = models.CharField(max_length=120, default="", blank=True)
    municipality = models.CharField(max_length=120, default="", blank=True)
    country_code = models.CharField(max_length=2, default="", blank=True)
    postal_code = models.IntegerField(null=True, blank=True)

    distances = models.JSONField(null=True, blank=True)
    test = models.JSONField(null=True, blank=True)

    unique_displayname_object = models.ForeignKey(
        to="UniqueLocationDisplayname",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="geotag_level_5_set",
    )

    class Meta:
        db_table = "geotag_level_5"

    def get_boundingbox_areal(self) -> float:
        return self.distances["ns"] * self.distances["ew"]

    @classmethod
    def new_from_dict(cls, geotag_dict: dict) -> object:
        if not geotag_dict or not isinstance(geotag_dict, dict):
            return None

        if "level_5" not in geotag_dict or not isinstance(geotag_dict["level_5"], dict):
            return None

        if not all(
            [
                "lat_min" in geotag_dict["level_5"],
                "lat_max" in geotag_dict["level_5"],
                "lng_min" in geotag_dict["level_5"],
                "lng_max" in geotag_dict["level_5"],
            ]
        ):
            return None

        existing = cls.objects.filter(
            lat_min=geotag_dict["level_5"]["lat_min"],
            lat_max=geotag_dict["level_5"]["lat_max"],
            lng_min=geotag_dict["level_5"]["lng_min"],
            lng_max=geotag_dict["level_5"]["lng_max"],
        ).first()

        if existing:
            return existing

        new_object = cls.objects.create(
            lat_min=geotag_dict["level_5"]["lat_min"],
            lat_max=geotag_dict["level_5"]["lat_max"],
            lng_min=geotag_dict["level_5"]["lng_min"],
            lng_max=geotag_dict["level_5"]["lng_max"],
            displayname_short=geotag_dict["level_5"]["displayname_short"],
            displayname_full=geotag_dict["level_5"]["displayname_full"],
            postal_town=geotag_dict["level_5"]["postal_town"],
            locality=geotag_dict["level_5"]["locality"],
            county=geotag_dict["level_5"]["county"],
            municipality=geotag_dict["level_5"]["municipality"],
            country_code=geotag_dict["level_5"]["country_code"],
            postal_code=geotag_dict["level_5"]["postal_code"],
            distances=geotag_dict["level_5"]["distances"],
        )

        return new_object

    @classmethod
    def get_by_bounds(cls, bbox_dict: dict) -> object:
        if not bbox_dict or not isinstance(bbox_dict, dict):
            return None

        if not all(
            [
                "lat_min" in bbox_dict,
                "lat_max" in bbox_dict,
                "lng_min" in bbox_dict,
                "lng_max" in bbox_dict,
            ]
        ):
            return None

        qs = cls.objects.filter(
            lat_min__lt=bbox_dict["lat_min"],
            lat_max__gt=bbox_dict["lat_max"],
            lng_min__lt=bbox_dict["lng_min"],
            lng_max__gt=bbox_dict["lng_max"],
        )

        if not qs.exists():
            return None

        obj = sorted(qs, key=lambda x: (x.get_boundingbox_areal()))[0]

        return obj


class GeotagLevel4(models.Model):
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

    displayname_short = models.CharField(max_length=255, default="", blank=True)
    displayname_full = models.CharField(max_length=255, default="", blank=True)

    postal_town = models.CharField(max_length=120, default="", blank=True)
    locality = models.CharField(max_length=120, default="", blank=True)
    county = models.CharField(max_length=120, default="", blank=True)
    municipality = models.CharField(max_length=120, default="", blank=True)
    country_code = models.CharField(max_length=2, default="", blank=True)
    postal_code = models.IntegerField(null=True, blank=True)

    distances = models.JSONField(null=True, blank=True)

    unique_displayname_object = models.ForeignKey(
        to="UniqueLocationDisplayname",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="geotag_level_4_set",
    )

    geotag_level_5 = models.ForeignKey(
        to="GeotagLevel5", null=True, blank=True, on_delete=models.CASCADE
    )

    class Meta:
        db_table = "geotag_level_4"

    def get_boundingbox_areal(self) -> float:
        return self.distances["ns"] * self.distances["ew"]

    @classmethod
    def new_from_dict(cls, geotag_dict: dict) -> object:
        if not geotag_dict or not isinstance(geotag_dict, dict):
            return None

        if "level_4" not in geotag_dict or not isinstance(geotag_dict["level_4"], dict):
            return None

        if not all(
            [
                "lat_min" in geotag_dict["level_4"],
                "lat_max" in geotag_dict["level_4"],
                "lng_min" in geotag_dict["level_4"],
                "lng_max" in geotag_dict["level_4"],
            ]
        ):
            return None

        existing = cls.objects.filter(
            lat_min=geotag_dict["level_4"]["lat_min"],
            lat_max=geotag_dict["level_4"]["lat_max"],
            lng_min=geotag_dict["level_4"]["lng_min"],
            lng_max=geotag_dict["level_4"]["lng_max"],
        ).first()

        if existing:
            return existing

        new_object = cls.objects.create(
            lat_min=geotag_dict["level_4"]["lat_min"],
            lat_max=geotag_dict["level_4"]["lat_max"],
            lng_min=geotag_dict["level_4"]["lng_min"],
            lng_max=geotag_dict["level_4"]["lng_max"],
            displayname_short=geotag_dict["level_4"]["displayname_short"],
            displayname_full=geotag_dict["level_4"]["displayname_full"],
            postal_town=geotag_dict["level_4"]["postal_town"],
            locality=geotag_dict["level_4"]["locality"],
            county=geotag_dict["level_4"]["county"],
            municipality=geotag_dict["level_4"]["municipality"],
            country_code=geotag_dict["level_4"]["country_code"],
            postal_code=geotag_dict["level_4"]["postal_code"],
            distances=geotag_dict["level_4"]["distances"],
        )

        level_5 = GeotagLevel5.get_by_bounds(
            dict(
                lat_min=geotag_dict["level_4"]["lat_min"],
                lat_max=geotag_dict["level_4"]["lat_max"],
                lng_min=geotag_dict["level_4"]["lng_min"],
                lng_max=geotag_dict["level_4"]["lng_max"],
            )
        )

        if not level_5:
            level_5 = GeotagLevel5.new_from_dict(geotag_dict)

        if level_5:
            new_object.geotag_level_5 = level_5
            new_object.save()

        return new_object

    @classmethod
    def get_by_bounds(cls, bbox_dict: dict) -> object:
        if not bbox_dict or not isinstance(bbox_dict, dict):
            return None
        if not all(
            [
                "lat_min" in bbox_dict,
                "lat_max" in bbox_dict,
                "lng_min" in bbox_dict,
                "lng_max" in bbox_dict,
            ]
        ):
            return None

        qs = cls.objects.filter(
            lat_min__lt=bbox_dict["lat_min"],
            lat_max__gt=bbox_dict["lat_max"],
            lng_min__lt=bbox_dict["lng_min"],
            lng_max__gt=bbox_dict["lng_max"],
        )

        if not qs.exists():
            return None

        obj = sorted(qs, key=lambda x: (x.get_boundingbox_areal()))[0]

        return obj


class GeotagLevel3(models.Model):
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

    displayname_short = models.CharField(max_length=255, default="", blank=True)
    displayname_full = models.CharField(max_length=255, default="", blank=True)

    postal_town = models.CharField(max_length=120, default="", blank=True)
    locality = models.CharField(max_length=120, default="", blank=True)
    county = models.CharField(max_length=120, default="", blank=True)
    municipality = models.CharField(max_length=120, default="", blank=True)
    country_code = models.CharField(max_length=2, default="", blank=True)
    postal_code = models.IntegerField(null=True, blank=True)

    distances = models.JSONField(null=True, blank=True)

    unique_displayname_object = models.ForeignKey(
        to="UniqueLocationDisplayname",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="geotag_level_3_set",
    )

    geotag_level_4 = models.ForeignKey(
        to="GeotagLevel4",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="geotag_level_3_set",
    )

    class Meta:
        db_table = "geotag_level_3"

    def get_boundingbox_areal(self) -> float:
        return self.distances["ns"] * self.distances["ew"]

    @classmethod
    def new_from_dict(cls, geotag_dict: dict) -> object:
        if not geotag_dict or not isinstance(geotag_dict, dict):
            return None

        if "level_3" not in geotag_dict or not isinstance(geotag_dict["level_3"], dict):
            return None

        if not all(
            [
                "lat_min" in geotag_dict["level_3"],
                "lat_max" in geotag_dict["level_3"],
                "lng_min" in geotag_dict["level_3"],
                "lng_max" in geotag_dict["level_3"],
            ]
        ):
            return None

        existing = cls.objects.filter(
            lat_min=geotag_dict["level_3"]["lat_min"],
            lat_max=geotag_dict["level_3"]["lat_max"],
            lng_min=geotag_dict["level_3"]["lng_min"],
            lng_max=geotag_dict["level_3"]["lng_max"],
        ).first()

        if existing:
            return existing

        new_object = cls.objects.create(
            lat_min=geotag_dict["level_3"]["lat_min"],
            lat_max=geotag_dict["level_3"]["lat_max"],
            lng_min=geotag_dict["level_3"]["lng_min"],
            lng_max=geotag_dict["level_3"]["lng_max"],
            displayname_short=geotag_dict["level_3"]["displayname_short"],
            displayname_full=geotag_dict["level_3"]["displayname_full"],
            postal_town=geotag_dict["level_3"]["postal_town"],
            locality=geotag_dict["level_3"]["locality"],
            county=geotag_dict["level_3"]["county"],
            municipality=geotag_dict["level_3"]["municipality"],
            country_code=geotag_dict["level_3"]["country_code"],
            postal_code=geotag_dict["level_3"]["postal_code"],
            distances=geotag_dict["level_3"]["distances"],
        )

        level_4 = GeotagLevel4.get_by_bounds(
            dict(
                lat_min=geotag_dict["level_3"]["lat_min"],
                lat_max=geotag_dict["level_3"]["lat_max"],
                lng_min=geotag_dict["level_3"]["lng_min"],
                lng_max=geotag_dict["level_3"]["lng_max"],
            )
        )

        if not level_4:
            level_4 = GeotagLevel4.new_from_dict(geotag_dict)

        if level_4:
            new_object.geotag_level_4 = level_4
            new_object.save()

        return new_object

    @classmethod
    def get_by_bounds(cls, bbox_dict: dict) -> object:
        if not bbox_dict or not isinstance(bbox_dict, dict):
            return None

        if not all(
            [
                "lat_min" in bbox_dict,
                "lat_max" in bbox_dict,
                "lng_min" in bbox_dict,
                "lng_max" in bbox_dict,
            ]
        ):
            return None

        qs = cls.objects.filter(
            lat_min__lt=bbox_dict["lat_min"],
            lat_max__gt=bbox_dict["lat_max"],
            lng_min__lt=bbox_dict["lng_min"],
            lng_max__gt=bbox_dict["lng_max"],
        )

        if not qs.exists():
            return None

        obj = sorted(qs, key=lambda x: (x.get_boundingbox_areal()))[0]

        return obj


class GeotagLevel2(models.Model):
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

    displayname_short = models.CharField(max_length=255, default="", blank=True)
    displayname_full = models.CharField(max_length=255, default="", blank=True)

    postal_town = models.CharField(max_length=120, default="", blank=True)
    locality = models.CharField(max_length=120, default="", blank=True)
    county = models.CharField(max_length=120, default="", blank=True)
    municipality = models.CharField(max_length=120, default="", blank=True)
    country_code = models.CharField(max_length=2, default="", blank=True)
    postal_code = models.IntegerField(null=True, blank=True)

    distances = models.JSONField(null=True, blank=True)

    unique_displayname_object = models.ForeignKey(
        to="UniqueLocationDisplayname",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="geotag_level_2_set",
    )

    geotag_level_3 = models.ForeignKey(
        to="GeotagLevel3",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="geotag_level_2_set",
    )

    class Meta:
        db_table = "geotag_level_2"

    def get_boundingbox_areal(self) -> float:
        return self.distances["ns"] * self.distances["ew"]

    @classmethod
    def new_from_dict(cls, geotag_dict: dict) -> object:
        if not geotag_dict or not isinstance(geotag_dict, dict):
            return None

        if "level_2" not in geotag_dict or not isinstance(geotag_dict["level_2"], dict):
            return None

        if not all(
            [
                "lat_min" in geotag_dict["level_2"],
                "lat_max" in geotag_dict["level_2"],
                "lng_min" in geotag_dict["level_2"],
                "lng_max" in geotag_dict["level_2"],
            ]
        ):
            return None

        existing = cls.objects.filter(
            lat_min=geotag_dict["level_2"]["lat_min"],
            lat_max=geotag_dict["level_2"]["lat_max"],
            lng_min=geotag_dict["level_2"]["lng_min"],
            lng_max=geotag_dict["level_2"]["lng_max"],
        ).first()

        if existing:
            return existing

        new_object = cls.objects.create(
            lat_min=geotag_dict["level_2"]["lat_min"],
            lat_max=geotag_dict["level_2"]["lat_max"],
            lng_min=geotag_dict["level_2"]["lng_min"],
            lng_max=geotag_dict["level_2"]["lng_max"],
            displayname_short=geotag_dict["level_2"]["displayname_short"],
            displayname_full=geotag_dict["level_2"]["displayname_full"],
            postal_town=geotag_dict["level_2"]["postal_town"],
            locality=geotag_dict["level_2"]["locality"],
            county=geotag_dict["level_2"]["county"],
            municipality=geotag_dict["level_2"]["municipality"],
            country_code=geotag_dict["level_2"]["country_code"],
            postal_code=geotag_dict["level_2"]["postal_code"],
            distances=geotag_dict["level_2"]["distances"],
        )

        level_3 = GeotagLevel3.get_by_bounds(
            dict(
                lat_min=geotag_dict["level_2"]["lat_min"],
                lat_max=geotag_dict["level_2"]["lat_max"],
                lng_min=geotag_dict["level_2"]["lng_min"],
                lng_max=geotag_dict["level_2"]["lng_max"],
            )
        )

        if not level_3:
            level_3 = GeotagLevel3.new_from_dict(geotag_dict)

        if level_3:
            new_object.geotag_level_3 = level_3
            new_object.save()

        return new_object

    @classmethod
    def get_by_bounds(cls, bbox_dict: dict) -> object:
        if not bbox_dict or not isinstance(bbox_dict, dict):
            return None
        if not all(
            [
                "lat_min" in bbox_dict,
                "lat_max" in bbox_dict,
                "lng_min" in bbox_dict,
                "lng_max" in bbox_dict,
            ]
        ):
            return None

        qs = cls.objects.filter(
            lat_min__lt=bbox_dict["lat_min"],
            lat_max__gt=bbox_dict["lat_max"],
            lng_min__lt=bbox_dict["lng_min"],
            lng_max__gt=bbox_dict["lng_max"],
        )

        if not qs.exists():
            return None

        obj = sorted(qs, key=lambda x: (x.get_boundingbox_areal()))[0]

        return obj


class GeotagLevel1(models.Model):
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

    displayname_short = models.CharField(max_length=255, default="", blank=True)
    displayname_full = models.CharField(max_length=255, default="", blank=True)

    postal_town = models.CharField(max_length=120, default="", blank=True)
    locality = models.CharField(max_length=120, default="", blank=True)
    county = models.CharField(max_length=120, default="", blank=True)
    municipality = models.CharField(max_length=120, default="", blank=True)
    country_code = models.CharField(max_length=2, default="", blank=True)
    postal_code = models.IntegerField(null=True, blank=True)

    distances = models.JSONField(null=True, blank=True)

    unique_displayname_object = models.ForeignKey(
        to="UniqueLocationDisplayname",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="geotag_level_1_set",
    )

    geotag_level_2 = models.ForeignKey(
        to="GeotagLevel2",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="geotag_level_1_set",
    )

    class Meta:
        db_table = "geotag_level_1_correct"

    def get_boundingbox_areal(self) -> float:
        return self.distances["ns"] * self.distances["ew"]

    def get_videoitems(self, limit: int):
        return [x.get_videoitems(limit) for x in self.gps_points.all()[:limit]]

    def get_displayname_short(self) -> str:
        list_ = self.displayname_short.split(",")
        dict_ = model_to_dict(self, fields=list_)

        displayname_short = ", ".join(
            dict_[x] for x in list_ if all([x is not None, dict_[x]])
        ).replace("fylke", "")

        return displayname_short.strip()

    @classmethod
    def new_from_dict(cls, geotag_dict: dict) -> object:
        if not geotag_dict or not isinstance(geotag_dict, dict):
            return None

        if "level_1" not in geotag_dict or not isinstance(geotag_dict["level_1"], dict):
            return None

        if not all(
            [
                "lat_min" in geotag_dict["level_1"],
                "lat_max" in geotag_dict["level_1"],
                "lng_min" in geotag_dict["level_1"],
                "lng_max" in geotag_dict["level_1"],
            ]
        ):
            return None

        existing = cls.objects.filter(
            lat_min=geotag_dict["level_1"]["lat_min"],
            lat_max=geotag_dict["level_1"]["lat_max"],
            lng_min=geotag_dict["level_1"]["lng_min"],
            lng_max=geotag_dict["level_1"]["lng_max"],
        ).first()

        if existing:
            return existing

        new_object = cls.objects.create(
            lat_min=geotag_dict["level_1"]["lat_min"],
            lat_max=geotag_dict["level_1"]["lat_max"],
            lng_min=geotag_dict["level_1"]["lng_min"],
            lng_max=geotag_dict["level_1"]["lng_max"],
            displayname_short=geotag_dict["level_1"]["displayname_short"],
            displayname_full=geotag_dict["level_1"]["displayname_full"],
            postal_town=geotag_dict["level_1"]["postal_town"],
            locality=geotag_dict["level_1"]["locality"],
            county=geotag_dict["level_1"]["county"],
            municipality=geotag_dict["level_1"]["municipality"],
            country_code=geotag_dict["level_1"]["country_code"],
            postal_code=geotag_dict["level_1"]["postal_code"],
            distances=geotag_dict["level_1"]["distances"],
        )

        level_2 = GeotagLevel2.get_by_bounds(
            dict(
                lat_min=geotag_dict["level_1"]["lat_min"],
                lat_max=geotag_dict["level_1"]["lat_max"],
                lng_min=geotag_dict["level_1"]["lng_min"],
                lng_max=geotag_dict["level_1"]["lng_max"],
            )
        )

        if not level_2:
            level_2 = GeotagLevel2.new_from_dict(geotag_dict)

        if level_2:
            new_object.geotag_level_2 = level_2
            new_object.save()

        return new_object

    @classmethod
    def get_by_latlng(cls, latlng: tuple) -> object:
        (lat, lng) = latlng

        qs = cls.objects.filter(
            lat_min__lt=lat, lat_max__gt=lat, lng_min__lt=lng, lng_max__gt=lng
        )

        if not qs.exists():
            return None

        obj = sorted(qs, key=lambda x: (x.get_boundingbox_areal()))[0]

        return obj


class GmapsGpsPoint(models.Model):
    lat = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)
    lng = models.DecimalField(max_digits=11, decimal_places=7, null=True, blank=True)
    geotag_level_1 = models.ForeignKey(
        to="GeotagLevel1",
        on_delete=models.CASCADE,
        related_name="gps_points",
        null=True,
        blank=True,
    )

    geotag_lvl_1 = models.ForeignKey(
        to="GeotagLvl1",
        on_delete=models.CASCADE,
        related_name="gps_points",
        null=True,
        blank=True,
    )

    custom_displayname = models.CharField(max_length=120, default="", blank=True)

    class Meta:
        db_table = "gmaps_gpspoint"

    def get_videoitems(self, limit: int):
        return self.videoitems.all()[:limit]

    def get_displayname_short(self) -> str:
        if self.custom_displayname:
            return self.custom_displayname
        if self.geotag_level_1:
            return self.geotag_level_1.get_displayname_short()

    @classmethod
    def get_by_latlng(cls, latlng: tuple) -> object:
        (lat, lng) = latlng
        bounds_2m = get_bounding_box(lat, lng, 0.0002)

        # flytte til QuerySet
        qs = GmapsGpsPoint.objects.filter(
            lat__gt=bounds_2m["lat_min"],
            lat__lt=bounds_2m["lat_max"],
            lng__gt=bounds_2m["lng_min"],
            lng__lt=bounds_2m["lng_max"],
        )

        obj = None
        if qs:
            for gps_point in qs:
                # snap to existing point within 1 meter
                if (
                    geopy.distance.distance(
                        latlng,
                        (
                            gps_point.lat,
                            gps_point.lng,
                        ),
                    ).meters
                    <= 1
                ):
                    obj = gps_point
                    break

        if obj is None:
            obj = GmapsGpsPoint.objects.create(lat=lat, lng=lng)

        if obj.geotag_level_1 is None:
            geotag = GeotagLevel1.get_by_latlng(latlng)
            geotag2 = Geotag.get_smallest_containing(latlng)
            if not geotag:
                ScheduledReverseGeotag.schedule_if_not_scheduled(obj)
            else:
                obj.geotag_level_1 = geotag
                obj.save()

        return obj
