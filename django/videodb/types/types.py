from decimal import Decimal
from typing import Literal, TypedDict, Optional, Union
from numbers import Real


LatLngTuple = tuple[Real]


class BoundingBoxDict(TypedDict):
    lat_min: Decimal
    lat_max: Decimal
    lng_min: Decimal
    lng_max: Decimal


class InclusionExclusionBoundingBoxDict(TypedDict, total=False):
    boundingbox: BoundingBoxDict
    exclude_outer: BoundingBoxDict


IncrementalBoundingBoxesDict = dict[str, InclusionExclusionBoundingBoxDict]


class AddressDict(TypedDict, total=False):
    country_code: Optional[str]
    county: Optional[str]
    locality: Optional[str]
    municipality: Optional[str]
    postal_town: Optional[str]
    postal_code: Optional[Union[str, int]]
    country: Optional[str]
    formatted_address: Optional[str]
    displayname_full: Optional[str]
    displayname_short: Optional[str]


class FieldValueNamedDict(TypedDict):
    field: str
    value: str


class AddressParentFieldsComparisonDict(TypedDict):
    obj_min_first_unique_parent: FieldValueNamedDict
    obj_max_first_unique_parent: FieldValueNamedDict


IdValueDict = dict[Union[str, int], Union[str, int]]

AddressFieldName = Literal[
    "country_code",
    "county",
    "locality",
    "postal_town",
    "municipality",
    "postal_town",
    "postal_code",
    "country",
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

AddressFieldValueDict = dict[AddressFieldName, Union[str, int]]

AddressNameGroupingsDict = dict[AddressFieldNameCombination, AddressFieldValueDict]
