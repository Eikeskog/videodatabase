from timeit import default_timer as timer
from rest_framework import serializers
from .utils.functions.videoitem import get_nearby_videoitems
from .models.videoitem import Videoitem
from .models.project import Project
from .models.local import Disk, LocalFile
from .models.videoitems_list import VideoitemsList
from .models.unique_searchfilter import (
    UniqueLocationDisplayname,
    UniqueKeyword,
    UniqueCamera,
    UniqueFps,
)


# def _reset_all_geotags() -> None:
#     ScheduledReverseGeotag.objects.all().delete()
#     Geotag.objects.all().delete

#     for obj in Videoitem.objects.filter(gps_lat__isnull=False):
#         point = (obj.gps_lat, obj.gps_lng)
#         GmapsGpsPoint.get_by_latlng(point)

#     ScheduledReverseGeotag.run_batch_reverse()


# def _show_sorted_geotag_areals() -> None:
#     geotags = []
#     geotag_cls = [GeotagLvl1, GeotagLvl2, GeotagLvl3, GeotagLvl4, GeotagLvl5]
#     for i, c in enumerate(geotag_cls):
#         geotags.append(list(c.objects.all().order_by('areal').values('id', 'areal')))
#         print(f'class {i+1}:')
#         print(geotags[i])
#         print(f'min? {geotags[i][0]} - max? {geotags[i][-1]}')


class UniqueSearchfiltersSerializer(serializers.ModelSerializer):
    class Meta:
        model = None

    def to_representation(self, *args, **kwargs):
        # Geotag.objects.all().delete()
        # GmapsGpsPoint.objects.all().delete()
        # ScheduledReverseGeotag.objects.all().delete()
        # ScheduledReverseGeotag.run_batch_reverse()

        # for x in Videoitem.objects.exclude(gps_lat__isnull=True):
        #     latlng = (x.gps_lat, x.gps_lng)
        #     x.gmaps_gps_point = GmapsGpsPoint.get_by_latlng(latlng)
        #     x.save()

        # UniqueLocationDisplayname._rebuild()
        # for x in UniqueLocationDisplayname.objects.all():
        #     # m_dict = model_to_dict(x)
        #     # addr = {k: v for k,v in json.loads(m_dict["unique_json"])["unique_fields_include_null"].items() if v}
        #     # print(addr)
        #     # # addr2 = x.unique_fields_not_null()
        #     x.link_to_geotags(addr)
        # print()
        # for x in UniqueLocationDisplayname._all_geotags_as_address_dicts():
        # for obj in UniqueLocationDisplayname.objects.all():
        #     obj.link_to_geotags(x)

        data = {}

        cameras = UniqueCamera.objects.all()[:15]
        keywords = UniqueKeyword.objects.all()[:15]
        projects = Project.objects.all()[:15]
        disks = Disk.objects.all()[:15]
        location_names = UniqueLocationDisplayname.objects.all().order_by(
            "most_specific_field_value"
        )[:15]

        fps_groups = {
            "24": [],
            "27-30": [],
            "48": [],
            "60": [],
            "120": [],
            "240": [],
            "other": [],
        }

        for obj in UniqueFps.objects.all():
            match = False
            for key in list(fps_groups.keys())[:-1]:
                if "-" not in key:
                    if obj.fps == int(key):
                        fps_groups[key].append(obj.id)
                        match = True
                        break
                else:
                    s = key.split("-")
                    if int(s[0]) <= obj.fps <= int(s[1]):
                        fps_groups[key].append(obj.id)
                        match = True
                        break
            if not match:
                fps_groups["other"].append(obj.id)

        data["dateRange"] = {
            "items": {},
        }

        data["camera"] = {
            "items": {obj.id: str(obj) for obj in cameras[:10]},
            "count": len(cameras),
        }

        data["fps"] = {
            "items": {",".join(str(x) for x in v): k for k, v in fps_groups.items()},
            "count": len(fps_groups),
        }

        data["keyword"] = {
            "items": {obj.id: str(obj) for obj in keywords[:10]},
            "count": len(keywords),
        }

        data["project"] = {
            "items": {str(obj.project_id): str(obj.name) for obj in projects[:10]},
            "count": len(projects),
        }

        data["disk"] = {
            "items": {str(obj.disk_serial_number): str(obj.name) for obj in disks[:10]},
            "count": len(disks),
        }

        data["location"] = {
            "items": {obj.id: str(obj) for obj in location_names[:10]},
            "count": len(location_names),
        }

        data["lists"] = {"items": {}}

        return data


class LocalFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalFile
        fields = ["path"]
        depth = 1

    def validate(self, data):
        return super().validate(data)

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data["project"] = instance.get_project()
        data["disk"] = instance.get_disk()
        data["directory"] = instance.get_directory()

        return data


class VideoitemsListSerializer(serializers.ModelSerializer):
    videoitems = serializers.SerializerMethodField()

    class Meta:
        model = VideoitemsList
        fields = "__all__"
        depth = 1

    def get_videoitems(self, obj):
        data = []
        # kontroll på user og filer her også.
        videoitems = obj.videoitems.all()
        for x in videoitems:
            data.append(
                {
                    "pk": x.pk,
                    "thumbnail_count": x.static_thumbnail_count,
                    "tags": [
                        {"pk": keyword.unique_keyword.pk, "label": keyword.keyword}
                        for keyword in x.keyword_set.all()
                    ],
                }
            )
        return data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["created_by"] = int(instance.created_by.id)
        return data


class VideoitemEntrySerializer(serializers.ModelSerializer):
    local_paths = LocalFileSerializer(many=True)
    user_lists = serializers.SerializerMethodField()

    class Meta:
        model = Videoitem
        fields = "__all__"
        depth = 2

    def get_user_lists(self, obj):
        try:
            request = self.context["request"]
            if not request.user.is_authenticated:
                return None
        except AttributeError:
            return None

        user = request.user
        user_lists = obj.videoitemslist_set.filter(created_by=user).values_list(
            "pk", flat=True
        )

        return user_lists

    def validate(self, data):
        return super().validate(data)

    def to_representation(self, instance):
        t0 = timer()
        data = super().to_representation(instance)
        data["location_displayname"] = instance.get_displayname_short()
        # nearby items er en liten bottleneck, tar 15-20 ms å kjøre sånn det er nå.
        # mulige alternativer for løsninger:
        # cache, bruke geospatial fields på modeller(gps-punkt og bbox)
        # eller forandre på frontend: eks webworker, lazy load.
        data["nearby_items"] = (
            get_nearby_videoitems(instance)
            if instance.gmaps_gps_point is not None
            else None
        )
        data["tags"] = instance.get_tags()
        data["location_suggestions"] = instance.get_gps_suggestions_local_dir()

        t1 = timer()
        print("elapsed:", t1 - t0)
        # print(data["nearby_items"])
        return data


class TypingHintsSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = None

    def validate(self, data):
        return super().validate(data)

    def to_representation(self, instance):
        data = {
            "label": str(instance),
            "id": str(instance.id),
        }
        try:
            if instance.temp_label:
                data["label"] = instance.temp_label
        except AttributeError:
            pass
        return data


class VideoitemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Videoitem
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["location_displayname_short"] = instance.get_displayname_short()

        return data
