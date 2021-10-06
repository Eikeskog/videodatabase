import json
from django.db import models
from .geotags import (
  GeotagLevel1,
  GeotagLevel2,
  GeotagLevel3,
  GeotagLevel4,
  GeotagLevel5
)

# early development
class UniqueSearchfilter(models.Model):
    pass

class UniqueCamera(UniqueSearchfilter):
    class Meta:
        db_table = 'unique_camera'
        ordering = ['camera']

    camera = models.CharField(max_length=120, unique=True, null=True, blank=True)
    camera_unique_searchfilter = models.OneToOneField(UniqueSearchfilter, on_delete=models.CASCADE, parent_link=True)
 
    def __str__(self):
        return str(self.camera)


class UniqueFps(UniqueSearchfilter):
    class Meta:
        db_table = 'unique_fps'
        ordering = ['fps']

    fps = models.IntegerField(unique=True, null=True, blank=True)
    fps_unique_searchfilter = models.OneToOneField(UniqueSearchfilter, on_delete=models.CASCADE, parent_link=True)

    def __str__(self):
        return str(self.fps)


class UniqueKeyword(UniqueSearchfilter):
    class Meta:
        db_table = 'unique_keyword'
        ordering = ['keyword']

    keyword = models.CharField(max_length=120, unique=True, null=True, blank=True)
    keyword_unique_searchfilter = models.OneToOneField(UniqueSearchfilter, on_delete=models.CASCADE, parent_link=True)

    def __str__(self):
        return str(self.keyword)


class UniqueLocationDisplayname(UniqueSearchfilter):
    class Meta:
        db_table = 'unique_location_displayname'
        ordering = ['most_specific_field_value']

    unique_json = models.JSONField(null=True, blank=True)

    most_specific_field = models.CharField(max_length=120, null=True, blank=True)
    most_specific_field_value = models.CharField(max_length=120, null=True, blank=True)

    alternative_name = models.CharField(max_length=255, null=True, blank=True)

    displayname_unique_searchfilter = models.OneToOneField(UniqueSearchfilter, on_delete=models.CASCADE, parent_link=True)

    videoitems = models.ManyToManyField(to='Videoitem')
    geotags = models.ManyToManyField(to='GeotagLevel1')
    gps_points = models.ManyToManyField(to='GmapsGpsPoint')


    @classmethod
    def get_unique_displaynames_any_address_field_startswith(cls, startswith: str, max: int = 10):
        # gjøre om til model fields istedetfor json, raskere søk
        results = {}
        c = 0
        for obj in cls.objects.all():
            for val in obj.get_unique_address_fields_not_null().values():
                if val.lower().startswith(startswith.lower()):
                    str_id = str(obj.id)
                    displayname = str(obj)
                    if str_id not in results and displayname not in results.values():
                        results[str_id] = displayname
                        c += 1
                        break
            if c == max:
                break

        return results

    def get_displayname_variants(self):
        return list(set(json.loads(self.unique_json)['displayname_variants']))

    @classmethod
    def sort_objs_on_min_max_address_fields_count(cls, objects_list: list) -> object:
        copy = [obj for obj in objects_list]
        copy.sort(key=lambda obj: len(obj.get_unique_address_fields_not_null().keys()))
        return copy

    def get_unique_address_fields_not_null(self):
        fields = json.loads(self.unique_json)['unique_fields_include_null']
        not_null = {
            key: value for key, value in fields.items() if value
        }
        return not_null

    @classmethod
    def compare_addresses_get_parent_difference(cls, obj_min_address_fields: dict, obj_max_address_fields: dict) -> dict:
        field_names = ['county', 'municipality', 'country_code']

        for field in field_names:
            if field in obj_min_address_fields and field in obj_max_address_fields:
                if obj_min_address_fields[field] != obj_max_address_fields[field]:
                    return {
                        'obj_min_first_unique_parent': {
                            'field' : field,
                            'value' : obj_min_address_fields[field]
                        },
                        'obj_max_first_unique_parent': {
                            'field' : field,
                            'value' : obj_max_address_fields[field]
                        }
                    }
        return None

    @classmethod
    def is_different_location(cls, obj_min_address_fields: dict, obj_max_address_fields: dict) -> bool:
        def check_field_difference(field_name):
            if field_name not in ['locality', 'postal_town'] and obj_min_address_fields[field_name] != obj_max_address_fields[field_name]:
                return True
            elif field_name == 'locality':
                if 'postal_town' in obj_max_address_fields:
                    if obj_min_address_fields['locality'] == obj_max_address_fields['postal_town']:
                        return False
                    else: 
                        return True
            elif field_name == 'postal_town':
                if 'locality' in obj_max_address_fields:
                    if obj_min_address_fields['postal_town'] == obj_max_address_fields['locality']:
                        return False
                    else:
                        return True

        for field_name in obj_min_address_fields.keys():
            if field_name not in obj_max_address_fields:
                if check_field_difference(field_name):
                    return True
            elif obj_min_address_fields[field_name] != obj_max_address_fields[field_name]:
                if check_field_difference(field_name):
                    return True
                    
        return False
        
    @classmethod
    def solve_name_clash(cls, existing_obj: object, new_obj: object) -> str:
        (obj_min, obj_max) = cls.sort_objs_on_min_max_address_fields_count([existing_obj, new_obj,])

        obj_min_address_fields = obj_min.get_unique_address_fields_not_null()
        obj_max_address_fields = obj_max.get_unique_address_fields_not_null()

        if not cls.is_different_location(obj_min_address_fields, obj_max_address_fields):
            new_obj.delete()
            return 'DELETED'
        
        parent_difference_obj = cls.compare_addresses_get_parent_difference(obj_min_address_fields, obj_max_address_fields)

        if not parent_difference_obj:
            new_obj.delete()
            return 'DELETED'

        obj_min_alt_name = f'{obj_min.most_specific_field_value}, {parent_difference_obj["obj_min_first_unique_parent"]["value"]}'
        obj_max_alt_name = f'{obj_max.most_specific_field_value}, {parent_difference_obj["obj_max_first_unique_parent"]["value"]}'

        if obj_min_alt_name == obj_max_alt_name:
            return 'ERROR'

        obj_min.alternative_name = obj_min_alt_name
        obj_min.save()
        obj_max.alternative_name = obj_max_alt_name
        obj_max.save()

        return 'SOLVED'

    def get_first_parent_field_value(self, from_field: str = None) -> str:
        child_parent_dict = dict(
            locality = ['postal_town', 'municipality', 'county'],
            postal_town = 'municipality',
            municipality = 'county',
            county = 'country_code',
            country_code = None,
        )

        if not from_field:
            from_field = self.most_specific_field

        if from_field == 'country_code':
            return None

        obj_fields_not_null = self.get_unique_address_fields_not_null()

        if len(obj_fields_not_null.keys()) == 1:
            return None
        
        if isinstance(from_field, list):
            parent_field = []
            for x in from_field:
                parent_field += child_parent_dict[x]
        else:
            parent_field = child_parent_dict[from_field]

        if isinstance(parent_field, str):
            if parent_field in obj_fields_not_null:
                return dict(
                    field = parent_field,
                    value = obj_fields_not_null[parent_field]
                )
            else:
                self.get_first_parent_field_value(from_field = parent_field)
        
        if isinstance(parent_field, list):
            for field in parent_field:
                if field in obj_fields_not_null:
                    return dict(
                        field = field,
                        value = obj_fields_not_null[field]
                    )
            for field in parent_field:
                self.get_first_parent_field_value(from_field = field)

    @classmethod
    # veldig røff sketch
    def rebuild(cls):
        def get_most_specific_field(_dict):
            first_key = list(_dict.keys())[0]
            most_specific_field = list(_dict[first_key].keys())[0]
            most_specific_field_value = _dict[first_key][list(_dict[first_key].keys())[0]]

            return [most_specific_field, most_specific_field_value]

        cls.objects.all().delete()

        geotag_classes = [GeotagLevel1, GeotagLevel2, GeotagLevel3, GeotagLevel4, GeotagLevel5]
        geotag_columns = ['postal_town', 'locality', 'municipality', 'county', 'country_code']
        geotags = []

        for geotag_class in geotag_classes:
            geotags += geotag_class.objects.all().values(*geotag_columns)

        unique_displayname_groupings_json = []

        for geotag in geotags:
            geotag_name_combinations = dict(
                postal_town_municipality = dict(
                    postal_town  = geotag['postal_town'],
                    municipality = geotag['municipality'],
                ),
                postal_town_locality = dict(
                    postal_town  = geotag['postal_town'],
                    locality     = geotag['locality'],
                ),
                postal_town_county = dict(
                    postal_town  = geotag['postal_town'],
                    county       = geotag['county'],
                ),
                locality_municipality = dict(
                    locality     = geotag['locality'],
                    municipality = geotag['municipality'],
                ),
                locality_county = dict(
                    locality     = geotag['locality'],
                    county       = geotag['county'],
                ),
                municipality_county = dict(
                    municipality = geotag['municipality'],
                    county       = geotag['county'],
                ),
                county_country = dict(
                    county       = geotag['county'],
                    country_code = geotag['country_code'],
                ),
                country_code = dict(
                    country_code = geotag['country_code'],
                ),
            )

            geotag_displayname_alternatives = {}

            for group, entries in geotag_name_combinations.items():
                parts = list(entries.values())
                if all(parts): 
                    geotag_displayname_alternatives[group] = {}
                    if len(parts) > 1 and parts[0] == parts[1]:
                        key = list(entries.keys())[0]
                        value = entries[key]
                        geotag_displayname_alternatives[group][key] = parts[0]
                    else:
                        for key, value in entries.items():
                            geotag_displayname_alternatives[group][key] = value

            geotag_displayname_alternatives['displayname_variants'] = sorted([
                ", ".join(
                    column
                        if column != geotag['country_code'] else "__country_code__" + column
                        for column in displayname_alt.values()
                    )
                for displayname_alt in geotag_displayname_alternatives.values()
            ])

            for column_value in geotag.values():
                if all([
                    column_value,
                    column_value != geotag['country_code'],
                    column_value not in geotag_displayname_alternatives['displayname_variants']
                ]):
                    geotag_displayname_alternatives['displayname_variants'].append(column_value)

            geotag_displayname_alternatives['unique_fields_include_null'] = {
                _key: _value for _key, _value in geotag.items()
            }

            _json = json.dumps(geotag_displayname_alternatives, sort_keys=True)

            if _json not in unique_displayname_groupings_json:
                unique_displayname_groupings_json.append(_json)
                geotag_displayname_alternatives['json'] = _json
            else:
                continue

            most_specific_field = get_most_specific_field(geotag_displayname_alternatives)

            existing_obj = cls.objects.filter(
                most_specific_field_value = most_specific_field[1],
            ).first()

            new_obj = cls.objects.create(
                unique_json = _json,
                most_specific_field = most_specific_field[0],
                most_specific_field_value = most_specific_field[1],
            )

            if existing_obj:
                solve_clash = cls.solve_name_clash(existing_obj, new_obj)
                saved_obj = existing_obj if solve_clash == 'DELETED' else new_obj
            else:
                saved_obj = new_obj
            
            for geotag_class in geotag_classes:
                qs = geotag_class.objects.filter(**geotag)
                for geotag_obj in qs:
                    geotag_obj.unique_displayname_object = saved_obj
                    geotag_obj.save()

    def get_videoitems_qs(self):
        ...

    def __str__(self):
        if self.alternative_name is None:
            return str(self.most_specific_field_value)
        return str(self.alternative_name)