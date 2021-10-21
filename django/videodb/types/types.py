from decimal import Decimal
from typing import Literal, TypedDict, Optional, Union
from numbers import Real


class AddressDict(TypedDict, total=False):
    plus_code: Optional[str]
    locality: Optional[str]
    postal_town: Optional[str]
    postal_code: Optional[Union[str, int]]
    municipality: Optional[str]
    county: Optional[str]
    country: Optional[str]
    country_code: Optional[str]

    displayname_full: str
    displayname_short: str

    formatted_address: Optional[str]


class BoundingBoxDict(TypedDict):
    lat_min: Decimal
    lat_max: Decimal
    lng_min: Decimal
    lng_max: Decimal


class InclusionExclusionBoundingBoxDict(TypedDict, total=False):
    boundingbox: BoundingBoxDict
    exclude_outer: BoundingBoxDict


IncrementalBoundingBoxesDict = dict[str, InclusionExclusionBoundingBoxDict]


class BoundingBoxDistancesDict(TypedDict):
    ne_sw: Real
    ns: Real
    ew: Real


class GeocodeDict(TypedDict):
    lat_min: Real
    lat_max: Real
    lng_min: Real
    lng_max: Real

    distances: BoundingBoxDistancesDict
    viewport: BoundingBoxDict

    plus_code: Optional[str]
    locality: Optional[str]
    postal_town: Optional[str]
    postal_code: Optional[Union[str, int]]
    municipality: Optional[str]
    county: Optional[str]
    country: Optional[str]
    country_code: Optional[str]

    displayname_full: str
    displayname_short: str

    formatted_address: Optional[str]


MultiLevelGeocodeDict = dict[str, GeocodeDict]


class FieldValueNamedDict(TypedDict):
    field: str
    value: str


class AddressParentFieldsComparisonDict(TypedDict):
    obj_min_first_unique_parent: FieldValueNamedDict
    obj_max_first_unique_parent: FieldValueNamedDict


LatLngTuple = tuple[Real, Real]

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
    "plus_code",
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

NumberOrNumbersList = Union[list[Real], Real]
