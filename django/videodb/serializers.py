
from timeit import default_timer as timer
from django.forms.models import model_to_dict

from django.http.response import JsonResponse
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
    UniqueFps)


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

        data["lists"] = {
            'items': {}
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


class VideoitemsListSerializer(serializers.ModelSerializer):
    videoitems = serializers.SerializerMethodField()

    class Meta:
        model = VideoitemsList
        fields = '__all__'
        depth = 1

    def get_videoitems(self, obj):
        videoitems = obj.videoitems.all().values('videoitem_id', 'static_thumbnail_count')
        return videoitems

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data



class VideoitemEntrySerializer(serializers.ModelSerializer):
    local_paths = LocalFileSerializer(many=True)
    videoitems_list_set = serializers.SerializerMethodField()

    class Meta:
        model = Videoitem
        fields = '__all__'
        depth = 2

    def get_videoitems_list_set(self, obj):
        # videoitems_list_set = obj.videoitems_list_set.all().values('id', 'modified', 'user_id', 'label')
        # return videoitems_list_set
        return '...'

    def validate(self, data):
        return super().validate(data)

    def to_representation(self, instance):
        t0 = timer()
        data = super().to_representation(instance)
        data['location_displayname'] = instance.get_displayname_short()
        # nearby items er en bottleneck som tar ca 100 ms å kjøre sånn det er nå. 

        # mulige alternativer for løsninger:
        # bruke geospatial fields på modeller(gps-punkt og bbox), cache, webworkers, lazy load.
        # selve funksjonen gjør også mye nå, så skrive om (kutte ned på hva den gjør) ... 
        data['nearby_items'] = get_nearby_videoitems(instance) if instance.gmaps_gps_point is not None else None
        data['tags'] = instance.get_tags()
        data['location_suggestions'] = instance.get_gps_suggestions_local_dir()

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

        return data