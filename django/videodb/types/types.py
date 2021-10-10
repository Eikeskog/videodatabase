from typing import Literal, TypedDict, Optional, Union
from ..models.geotags import (
    GeotagLevel1,
    GeotagLevel2,
    GeotagLevel3,
    GeotagLevel4,
    GeotagLevel5,
)


class AddressDict(TypedDict, total=False):
    country_code: Optional[str]
    county: Optional[str]
    locality: Optional[str]
    municipality: Optional[str]
    postal_town: Optional[str]


class FieldValueNamedDict(TypedDict):
    field: str
    value: str


class AddressParentFieldsComparisonDict(TypedDict):
    obj_min_first_unique_parent: FieldValueNamedDict
    obj_max_first_unique_parent: FieldValueNamedDict


IdValueDict = dict[Union[str, int], Union[str, int]]

AddressFieldName = Literal[
    "country_code", "county", "locality", "postal_town", "municipality"
]

AddressFieldNameCombination = Literal[
    "postal_town_municipality",
    "postal_town_locality",
    "postal_town_county",
    "locality_municipality",
    "locality_county",
    "municipality_county",
    "county_country",
    "country_code",
]

AnyGeotag = Union[GeotagLevel1, GeotagLevel2, GeotagLevel3, GeotagLevel4, GeotagLevel5]

AddressFieldValueDict = dict[AddressFieldName, Union[str, int]]

AddressNameGroupingsDict = dict[AddressFieldNameCombination, AddressFieldValueDict]
