from django.db import models
from django.db.models.expressions import F
from .geotags import GmapsGpsPoint
from .local import LocalFile


class Videoitem(models.Model):
    class Meta:
        db_table = "videoitem"
        ordering = ["-exif_last_modified"]

    videoitem_id = models.CharField(max_length=16, primary_key=True)
    static_thumbnail_count = models.IntegerField(null=True, blank=True)

    exif_camera = models.CharField(max_length=120, default="", blank=True)
    exif_dimensions = models.CharField(max_length=120, default="", blank=True)
    exif_duration_hhmmss = models.CharField(max_length=120, default="", blank=True)
    exif_duration_sec = models.IntegerField(null=True, blank=True)
    exif_fps = models.DecimalField(
        max_digits=7, decimal_places=3, null=True, blank=True
    )
    exif_resolution = models.CharField(max_length=120, default="", blank=True)
    exif_last_modified = models.DateTimeField(null=True, blank=True)

    gps_lat = models.DecimalField(
        max_digits=11, decimal_places=7, null=True, blank=True
    )
    gps_lng = models.DecimalField(
        max_digits=11, decimal_places=7, null=True, blank=True
    )
    gmaps_gps_point = models.ForeignKey(
        to=GmapsGpsPoint,
        related_name="videoitems",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    users = models.ManyToManyField(to="core_user.User")
    lists = models.ManyToManyField(to="VideoitemsList")

    def __str__(self) -> str:
        return self.videoitem_id

    def get_tags(self) -> dict:
        return (
            self.keyword_set.all()
            .annotate(
                tag_id=F("id"),
                tag_label=F("keyword"),
            )
            .values(
                "tag_id",
                "tag_label",
            )
        )

    def get_gps_suggestions_local_dir(self) -> dict:
        data = (
            LocalFile.objects.filter(
                directory_id__in=self.local_paths.all()
                .select_related("directory")
                .values_list("directory_id", flat=True)
            )
            .select_related("videoitem")
            .exclude(videoitem__gmaps_gps_point__isnull=True)
            .annotate(
                gps_point_id=F("videoitem_id__gmaps_gps_point"),
                lat=F("videoitem_id__gmaps_gps_point_id__lat"),
                lng=F("videoitem_id__gmaps_gps_point_id__lng"),
                displayname_id=F(
                    "videoitem_id__"
                    "gmaps_gps_point_id__"
                    "geotag_level_1_id__"
                    "unique_displayname_object"
                ),
            )
            .values("gps_point_id", "lat", "lng", "displayname_id")
        )

        # response = []
        # for row in data:
        #     for key, val in row.items():
        #         if key == 'geotag_id':
        #             obj = GeotagLevel1.objects.get(pk=val)
        #             print(obj.get_displayname_short())
        #       if key == 'displayname_id':
        #           obj = UniqueLocationDisplayname.objects.get(pk=val)
        #           print(obj.get_displayname_variants())
        #           print(obj.most_specific_field_value)
        #           print([obj.get_displayname_short()
        #                   for obj in obj.geotaglevel1_set.all()])

        return data

    def get_latlng_tuple(self) -> tuple:
        return (
            self.gps_lat,
            self.gps_lng,
        )

    def get_displayname_short(self) -> str:
        if self.gmaps_gps_point:
            return self.gmaps_gps_point.get_displayname_short()

    def append_to_lists(self, user, videoitems_lists) -> None:
        print("append from user:", user)
        print("videoitems_lists:", videoitems_lists)

    def remove_from_lists(self, user, videoitems_lists) -> None:
        print("remove from user:", user)
        print("videoitems_lists:", videoitems_lists)
