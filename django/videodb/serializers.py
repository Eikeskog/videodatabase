from rest_framework import serializers
from .utils.functions.videoitem import get_nearby_videoitems 
from .models.videoitem import Videoitem
from .models.project import Project
from .models.unique_searchfilter import (
    UniqueLocationDisplayname,
    UniqueKeyword,
    UniqueCamera,
    UniqueFps)
from .models.local import (
    Disk,
    # LocalDirectory,
    # ProjectRollDirectory,
    LocalFile
)
from timeit import default_timer as timer

class UniqueSearchfiltersSerializer(serializers.ModelSerializer):
    class Meta:
        model = None

    # gjøre om det her til en cache 
    # slik at ikke alle operasjonene trengs
    # å gjøres unødvendig hver gang.

    def to_representation(self, *args, **kwargs):
        data = {}

        cameras = UniqueCamera.objects.all()[:15]
        keywords = UniqueKeyword.objects.all()[:15]
        projects = Project.objects.all()[:15]
        disks = Disk.objects.all()[:15]
        location_names = UniqueLocationDisplayname.objects.all().order_by('most_specific_field_value')[:15]

        fps_groups = {
            '24': [],
            '27-30': [],
            '48': [],
            '60': [],
            '120': [],
            '240': [],
            'other': []
        }

        for obj in UniqueFps.objects.all():
            match = False
            for key in list(fps_groups.keys())[:-1]:
                if not "-" in key:
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
                fps_groups['other'].append(obj.id)

        data["dateRange"] = {
            'items': {
            },
        }

        data["camera"] = {
            'items': {
                obj.id : str(obj)
                for obj in cameras[:10]
            },
            'count': len(cameras),
        }

        data["fps"] = {
            'items': {
                ",".join(str(x) for x in v) : k
                for k, v in fps_groups.items()
            },
            'count': len(fps_groups),
        }

        data["keyword"] = {
            'items': {
                obj.id : str(obj)
                for obj in keywords[:10]
            },
            'count': len(keywords),
        }

        data["project"] = {
            'items': {
                str(obj.project_id) : str(obj.name)
                for obj in projects[:10]
            },
            'count': len(projects),
        }

        data["disk"] = {
            'items': {
                str(obj.disk_serial_number) : str(obj.name)
                for obj in disks[:10]
            },
            'count': len(disks),
        }
        
        data["location"] = {
            'items': {
                obj.id : str(obj)
                for obj in location_names[:10]
            },
            'count': len(location_names),
        }

        return data


class LocalFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalFile
        fields = ['path']
        depth = 1

    def validate(self, data):
        return super().validate(data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['project'] = instance.get_project()
        data['disk'] = instance.get_disk()
        data['directory'] = instance.get_directory()
        return data


class VideoitemEntrySerializer(serializers.ModelSerializer):
    local_paths = LocalFileSerializer(many=True)

    class Meta:
        model = Videoitem
        fields = '__all__'
        depth = 2

    def validate(self, data):
        return super().validate(data)

    def to_representation(self, instance):
        t0 = timer()
        data = super().to_representation(instance)
        data['location_displayname'] = instance.get_displayname_short()
        data['nearby_items'] = get_nearby_videoitems(instance) if instance.gmaps_gps_point is not None else None
        data['tags'] = instance.get_tags()
        data['location_suggestions'] = instance.get_gps_suggestions_from_local_dir()

        # data['test'] = instance.local_paths.all().select_related('directory').values_list(flat=True)

        # test
        # test = UniqueLocationDisplayname.get_unique_displaynames_any_field_startswith('agder')
        # print(test)
        # test = GeotagLevel1.objects.all()[:3]

        # for obj in Videoitem.objects.exclude(gps_lat__isnull=True):
        #     if obj.gmaps_gps_point:
        #         gps = obj.gmaps_gps_point 
        #         obj.gmaps_gps_point = None
        #         obj.save()
        #         gps.delete()
        
        # test2 = sorted(
        #     GeotagLevel1.objects.all()[:3],
        #     key=lambda x: (x.get_boundingbox_areal()) # and if gross is the same, for the gross same objects, x.updated and then update was also the same, x.pk,
        # )

        # print('\n\n\n\nTESTING:\n')
        # for t in test2:
        #     print(t.get_boundingbox_areal())

        t1 = timer()
        print('elapsed:',t1-t0)
        return data




class TypingHintsSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields  = None

    def validate(self, data):
        return super().validate(data)

    def to_representation(self, instance):
        data = {
            'label': str(instance),
            'id': str(instance.id),
        }
        return data

class VideoitemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Videoitem
        fields = '__all__'

    def validate(self, data):
        return super().validate(data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["location_displayname_short"] = instance.get_displayname_short()
        # instance.gmaps_gps_point = None
        # instance.save()
        # if instance.gmaps_gps_point is not None:
        #     gps_point = instance.gmaps_gps_point
        #     instance.gmaps_gps_point = None
        #     instance.save()
        #     gps_point.delete()
        

        return data