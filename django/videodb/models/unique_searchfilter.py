from enum import Enum
import json
from typing import Optional, Type, TypeVar, Union  # , TypedDict
from django.db import models
from django.db.models.base import Model
from ..types.enums import StatusMessage
from .geotags import (
    GeotagLevel1,
    GeotagLevel2,
    GeotagLevel3,
    GeotagLevel4,
    GeotagLevel5,
)
from ..types.types import (
    AddressDict,
    AddressFieldName,
    AddressFieldNameCombination,
    AddressFieldValueDict,
    AddressNameGroupingsDict,
    AddressParentFieldsComparisonDict,
    AnyGeotag,
    FieldValueNamedDict,
    # AddressDict,
    IdValueDict,
)

SORTED_ADDR_FIELDS = [  # Most to least precise address field.
    "locality",
    "postal_town",
    "municipality",
    "county",
    "country_code",
]

ADDR_FIELDS_CHILD_PARENT = {
    "locality": ["postal_town", "municipality", "county"],
    "postal_town": "municipality",
    "municipality": "county",
    "county": "country_code",
    "country_code": None,
}

GEOTAG_CLASSES = [
    GeotagLevel1,
    GeotagLevel2,
    GeotagLevel3,
    GeotagLevel4,
    GeotagLevel5,
]


T = TypeVar("T", bound=Model)


# in early development
class UniqueSearchfilter(models.Model):
    pass


class UniqueCamera(UniqueSearchfilter):
    class Meta:
        db_table = "unique_camera"
        ordering = ["camera"]

    camera = models.CharField(max_length=120, unique=True, null=True, blank=True)
    camera_unique_searchfilter = models.OneToOneField(
        UniqueSearchfilter, on_delete=models.CASCADE, parent_link=True
    )

    def __str__(self):
        return str(self.camera)


class UniqueFps(UniqueSearchfilter):
    class Meta:
        db_table = "unique_fps"
        ordering = ["fps"]

    fps = models.IntegerField(unique=True, null=True, blank=True)
    fps_unique_searchfilter = models.OneToOneField(
        UniqueSearchfilter, on_delete=models.CASCADE, parent_link=True
    )

    def __str__(self):
        return str(self.fps)


class UniqueKeyword(UniqueSearchfilter):
    class Meta:
        db_table = "unique_keyword"
        ordering = ["keyword"]

    keyword = models.CharField(max_length=120, unique=True, null=True, blank=True)
    keyword_unique_searchfilter = models.OneToOneField(
        UniqueSearchfilter, on_delete=models.CASCADE, parent_link=True
    )

    def __str__(self):
        return self.keyword


class UniqueLocationDisplayname(UniqueSearchfilter):
    class Meta:
        db_table = "unique_location_displayname"
        ordering = ["most_specific_field_value"]

    unique_json = models.JSONField(null=True, blank=True)

    # add new field, or change these to 'most_preferred_field'
    most_specific_field = models.CharField(max_length=120, null=True, blank=True)
    most_specific_field_value = models.CharField(max_length=120, null=True, blank=True)

    alternative_name = models.CharField(max_length=255, null=True, blank=True)

    displayname_unique_searchfilter = models.OneToOneField(
        UniqueSearchfilter, on_delete=models.CASCADE, parent_link=True
    )

    videoitems = models.ManyToManyField(to="Videoitem")
    geotags = models.ManyToManyField(to="GeotagLevel1")
    gps_points = models.ManyToManyField(to="GmapsGpsPoint")

    @classmethod
    def get_id_value_any_field_startswith(
        cls, str_startswith: str, limit: int = 10
    ) -> IdValueDict:
        # gjøre om til model fields istedetfor json? raskere søk
        id_values = {}
        c = 0
        for obj in cls.objects.all():
            for val in obj.get_unique_address_fields_not_null().values():
                if val.lower().startswith(str_startswith.lower()):
                    (str_id, displayname) = (str(obj.id), str(obj))
                    if (
                        str_id not in id_values
                        and displayname not in id_values.values()
                    ):
                        id_values[str_id] = (
                            f"{displayname} ({val})"
                            if displayname != val
                            else displayname
                        )
                        c += 1
                        break
            if c == limit:
                break

        return id_values

    def get_displayname_variants(self) -> list[str]:
        return list(set(json.loads(self.unique_json)["displayname_variants"]))

    def get_unique_address_fields_not_null(self) -> AddressDict:
        fields = json.loads(self.unique_json)["unique_fields_include_null"]
        not_null = {key: value for key, value in fields.items() if value}
        return not_null

    @classmethod
    def sort_objs_on_min_max_address_fields_count(
        cls: Type[T] = None, objects: tuple[T] = None
    ) -> Optional[tuple[T]]:
        if objects is None:
            return None
        objs = list(objects)
        objs.sort(key=lambda obj: len(obj.get_unique_address_fields_not_null().keys()))
        return tuple(objs)

    @classmethod
    def compare_addresses_get_parent_field_difference(
        cls,
        obj_min_address_dict: AddressDict = None,
        obj_max_address_dict: AddressDict = None,
    ) -> Optional[AddressParentFieldsComparisonDict]:
        """
        Helper method used to solve duplicate displaynames.

        Compares two address dicts, which are different locations,
        but share most precise field value.

        Searches upwards in both address dicts to find the
        first parent field difference.
        """

        field_names = ["county", "municipality", "country_code"]

        field_name: AddressFieldName
        for field_name in field_names:
            if (
                field_name in obj_min_address_dict
                and field_name in obj_max_address_dict
            ) and (
                obj_min_address_dict[field_name] != obj_max_address_dict[field_name]
            ):
                return {
                    "obj_min_first_unique_parent": {
                        "field": field_name,
                        "value": obj_min_address_dict[field_name],
                    },
                    "obj_max_first_unique_parent": {
                        "field": field_name,
                        "value": obj_max_address_dict[field_name],
                    },
                }
        return None

    @classmethod
    def address_field_difference(
        address_dict1: AddressDict,
        address_dict2: AddressDict,
        field_name: AddressFieldName,
    ) -> bool:
        """
        Compares a single field in two address dicts.
        Returns true if field values are different.

        Locality and postal_town are treated as aliases,
        so will return false if locality == postal_town.
        """

        if field_name not in ["locality", "postal_town"]:
            if address_dict1[field_name] != address_dict2[field_name]:
                return True
            return False

        if field_name == "locality":
            if "postal_town" in field_name:
                if address_dict1["locality"] == address_dict2["postal_town"]:
                    return False
                return True

        if field_name == "postal_town":
            if "locality" in address_dict2:
                if address_dict1["postal_town"] == address_dict2["locality"]:
                    return False
                return True

    @classmethod
    def is_different_location(
        cls, address_dict_min: AddressDict, address_dict_max: AddressDict
    ) -> bool:
        """
        Compares two address dicts field for field.

        Dicts must be sorted on field count,
        so that the dict with least number of fields
        (lowest precision) can be used as reference.

        Returns true if difference in any fields,
        but treats postal_town and locality as aliases.
        """

        field_name: AddressFieldName
        for field_name in address_dict_min.keys():
            if field_name not in address_dict_max:
                if cls.address_field_difference(
                    address_dict_min, address_dict_max, field_name
                ):
                    return True
            if address_dict_min[field_name] != address_dict_max[field_name]:
                if cls.address_field_difference(
                    address_dict_min, address_dict_max, field_name
                ):
                    return True
        return False

    @classmethod
    def solve_name_clash(
        cls: Type[T] = None, existing_obj: T = None, new_obj: T = None
    ) -> StatusMessage:
        """
        Tries to solve cases where a displayname for a newly created instance
        clashes with the displayname of an already existing instance.
        """

        (obj_min, obj_max) = cls.sort_objs_on_min_max_address_fields_count(
            (existing_obj, new_obj)
        )

        obj_min_address_fields: AddressDict = (
            obj_min.get_unique_address_fields_not_null()
        )
        obj_max_address_fields: AddressDict = (
            obj_max.get_unique_address_fields_not_null()
        )

        if not cls.is_different_location(
            obj_min_address_fields, obj_max_address_fields
        ):
            new_obj.delete()
            return StatusMessage.DELETED

        parent_difference: bool = cls.compare_addresses_get_parent_field_difference(
            obj_min_address_fields, obj_max_address_fields
        )

        if not parent_difference:
            new_obj.delete()
            return StatusMessage.DELETED

        obj_min_alt_name: str = (
            f"{obj_min.most_specific_field_value}, "
            f'({parent_difference["obj_min_first_unique_parent"]["value"]})'
        )
        obj_max_alt_name: str = (
            f"{obj_max.most_specific_field_value}, "
            f'{parent_difference["obj_max_first_unique_parent"]["value"]}'
        )

        if obj_min_alt_name == obj_max_alt_name:
            return StatusMessage.ERROR

        obj_min.alternative_name = obj_min_alt_name
        obj_min.save()
        obj_max.alternative_name = obj_max_alt_name
        obj_max.save()

        return StatusMessage.SOLVED

    def get_first_parent_field_value(
        self,
        from_field: Union[AddressFieldName, list[AddressFieldName]] = None,
    ) -> Optional[FieldValueNamedDict]:
        """
        Returns closest parent value of any starting address field
        in a class instance.

        Allows multiple alternatives for parents.
        """

        if from_field is None:
            from_field = self.most_specific_field

        obj_fields_not_null = self.get_unique_address_fields_not_null()

        if from_field == "country_code" or len(obj_fields_not_null.keys()) == 1:
            return None

        if isinstance(from_field, list):
            parent_field: list[AddressFieldName] = [
                ADDR_FIELDS_CHILD_PARENT[x] for x in from_field
            ]
        else:
            parent_field: AddressFieldName = ADDR_FIELDS_CHILD_PARENT[from_field]

        if isinstance(parent_field, str):
            if parent_field in obj_fields_not_null:
                return {
                    "field": parent_field,
                    "value": obj_fields_not_null[parent_field],
                }
            self.get_first_parent_field_value(from_field=parent_field)

        if isinstance(parent_field, list):
            for field in parent_field:
                if field in obj_fields_not_null:
                    return {"field": field, "value": obj_fields_not_null[field]}
            for field in parent_field:
                self.get_first_parent_field_value(from_field=field)

    @classmethod
    def get_name_groupings_dict(
        cls, address_dict: AddressDict
    ) -> AddressNameGroupingsDict:
        """
        Returns a handful of address fields duos.

        Sorted by personal taste, from most to least preferred combinations.
        """
        return {
            "postal_town_municipality": {
                "postal_town": address_dict["postal_town"],
                "municipality": address_dict["municipality"],
            },
            "postal_town_locality": {
                "postal_town": address_dict["postal_town"],
                "locality": address_dict["locality"],
            },
            "postal_town_county": {
                "postal_town": address_dict["postal_town"],
                "county": address_dict["county"],
            },
            "locality_municipality": {
                "locality": address_dict["locality"],
                "municipality": address_dict["municipality"],
            },
            "locality_county": {
                "locality": address_dict["locality"],
                "county": address_dict["county"],
            },
            "municipality_county": {
                "municipality": address_dict["municipality"],
                "county": address_dict["county"],
            },
            "county_country": {
                "county": address_dict["county"],
                "country_code": address_dict["country_code"],
            },
            "country_code": {
                "country_code": address_dict["country_code"],
            },
        }

    @classmethod
    def get_preferred_field(
        cls,
        groupings: AddressNameGroupingsDict,
    ) -> tuple[AddressFieldName, Union[int, str]]:
        first_combination: AddressFieldNameCombination = list(groupings.keys())[0]

        # note: index over preferences should be outside class scope.
        field = list(groupings[first_combination].keys())[0]
        value = groupings[first_combination][
            list(groupings[first_combination].keys())[0]
        ]

        return (field, value)

    @classmethod
    def displayname_variants_from_address_dict(
        cls, address_dict: AddressDict
    ) -> list[str]:
        """
        Builds shortened location displayname strings,
        both from single field values (postal_town,
        county, etc.), and comma seperated combinations.

        Compares values in a given combination,
        uses only one if values are the same.
        Example: "Oslo, Oslo" becomes "Oslo".
        """

        groupings: AddressNameGroupingsDict = cls.get_name_groupings_dict(address_dict)
        variants = {}

        combo: AddressFieldNameCombination
        fields: AddressFieldValueDict
        for combo, fields in groupings.items():
            values = list(fields.values())
            if all(values):
                variants[combo] = {}
                if len(values) > 1 and values[0] == values[1]:
                    key = list(fields.keys())[0]
                    value = fields[key]
                    variants[combo][key] = values[0]
                else:
                    for key, value in fields.items():
                        variants[combo][key] = value

        displayname_variants = sorted(
            [
                ", ".join(
                    column
                    if column != address_dict["country_code"]
                    else "__country_code__" + column
                    for column in displayname_alt.values()
                )
                for displayname_alt in variants.values()
            ]
        )

        for column_value in address_dict.values():
            if all(
                [
                    column_value,
                    column_value != address_dict["country_code"],
                    column_value not in displayname_variants,
                ]
            ):
                displayname_variants.append(column_value)

        return displayname_variants

    @classmethod
    def all_geotags_as_address_dicts(cls) -> list[AddressDict]:
        dicts = []
        for _class in GEOTAG_CLASSES:
            dicts += _class.objects.all().values(*SORTED_ADDR_FIELDS)
        return dicts

    def link_to_geotags(self, address: AddressDict) -> None:
        for _class in GEOTAG_CLASSES:
            for obj in _class.objects.filter(**address):
                obj.unique_displayname_object = self
                obj.save()

    # needs refactoring
    @classmethod
    def rebuild(cls):
        cls.objects.all().delete()

        unique_displayname_groupings_json = []
        geotags_as_address_dicts = cls.all_geotags_as_address_dicts()

        for address_dict in geotags_as_address_dicts:
            name_variations = {}
            name_variations[
                "displayname_variants"
            ] = cls.displayname_variants_from_address_dict(address_dict)
            name_variations["unique_fields_include_null"] = dict(address_dict.items())

            as_json = json.dumps(name_variations, sort_keys=True)

            if as_json not in unique_displayname_groupings_json:
                unique_displayname_groupings_json.append(as_json)
                name_variations["json"] = as_json
            else:
                continue

            preferred_field = cls.get_preferred_field(
                name_variations["displayname_variants"]
            )

            existing_obj = cls.objects.filter(
                most_specific_field_value=preferred_field[1],
            ).first()

            new_obj = cls.objects.create(
                unique_json=as_json,
                most_specific_field=preferred_field[0],
                most_specific_field_value=preferred_field[1],
            )

            if existing_obj:
                solve_clash = cls.solve_name_clash(existing_obj, new_obj)
                saved_obj = (
                    existing_obj if solve_clash == StatusMessage.DELETED else new_obj
                )
            else:
                saved_obj = new_obj

            saved_obj.link_to_geotags(address_dict=address_dict)

    def get_videoitems_qs(self):
        ...

    def __str__(self):
        if self.alternative_name is None:
            return str(self.most_specific_field_value)
        return str(self.alternative_name)
