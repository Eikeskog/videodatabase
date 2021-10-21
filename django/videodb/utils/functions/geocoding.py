import re
from typing import Optional
from googlemaps import Client as GoogleMapsClient
from geopy import distance, Point

try:
    from backend.dev_settings import GMAPS_TOKEN
    from ...types.types import AddressDict, LatLngTuple, GeocodeDict, BoundingBoxDict
except ModuleNotFoundError:
    from dev_settings import GMAPS_TOKEN
    from dev_types import AddressDict, LatLngTuple, GeocodeDict, BoundingBoxDict


COMPONENT_TYPE_TRANSLL = {
    "administrative_area_level_2": "municipality",
    "administrative_area_level_1": "county",
}

COUNTRY_CODES = {"NORWAY": "NO"}

REMOVE_WORDS = [
    "Fylke",
    "fylke",
    "Kommune",
    "kommune",
    "Municipality",
    "municipality",
    "County",
    "county",
]

DISPLAYNAME_EXCLUDE = [
    "postal_code",
    "street_number",
    "displayname_short",
    "displayname_full",
    "formatted_address",
    "country",
    "plus_code",
]

PREPEND_COUNTRY_CODE = "COUNTRY_CODE__"

DISPLAYNAME_SHORT_POS1 = ["postal_town", "locality", "municipality", "county"]

DISPLAYNAME_SHORT_POS2 = ["county", "municipality", "country_code"]

ADDR_DICT_KEYS = [
    "displayname_full",
    "displayname_short",
    "locality",
    "postal_town",
    "county",
    "municipality",
    "country",
    "postal_code",
    "formatted_address",
    "country_code",
]

NE = "northeast"
SW = "southwest"

LAT = "lat"
LNG = "lng"

LVL_KEY_PREPEND = "level_"

NULL = [None, "", " "]


def gmaps_geocode_get_viewport(viewport_json: dict) -> Optional[BoundingBoxDict]:
    viewport = None
    if viewport_json[NE] and viewport_json[SW]:
        lat = (viewport_json[NE][LAT], viewport_json[SW][LAT])
        lng = (viewport_json[NE][LNG], viewport_json[SW][LNG])
        if all([*lat, *lng]):
            viewport = {
                "lat_min": min(lat),
                "lat_max": max(lat),
                "lng_min": min(lng),
                "lng_max": max(lng),
            }
    return viewport


def gmaps_geocode_get_address_dict(
    gmaps_address_components_json: dict,
) -> Optional[AddressDict]:
    if gmaps_address_components_json is None:
        return None

    def clean_str(string) -> str:
        for word in REMOVE_WORDS:
            string = string.replace(word, "").strip()
        return string

    def get_component_type(component_json: dict) -> str:
        return str(
            max(
                [type for type in component_json["types"] if type != "political"],
                key=len,
            )
            if len(component_json["types"]) > 0
            else component_json["types"][0]
        )

    def get_column_name(component_json: dict) -> str:
        component_type = get_component_type(component_json)
        if component_type in COMPONENT_TYPE_TRANSLL:
            return COMPONENT_TYPE_TRANSLL[component_type]
        return component_type

    def get_component_value(component_json: dict) -> str:
        return clean_str(
            max({component_json["short_name"], component_json["long_name"]})
        )

    def add_missing_dict_keys(addr_dict: AddressDict) -> AddressDict:
        full_addr_dict = {
            **addr_dict,
            **{x: None for x in ADDR_DICT_KEYS if x not in addr_dict.keys()},
        }
        return full_addr_dict

    address_dict = add_missing_dict_keys(
        {
            get_column_name(component): get_component_value(component)
            for component in gmaps_address_components_json
        }
    )

    address_dict["country_code"] = [
        component["short_name"]
        for component in gmaps_address_components_json
        if "country" in component["types"]
    ][0]

    displaynames = gmaps_geocode_get_displaynames(address_dict)

    return {**address_dict, **displaynames}


def get_displayname_full(
    address_dict: AddressDict, exclude=None
) -> Optional[str]:
    if exclude is None:
        exclude = DISPLAYNAME_EXCLUDE
    positions = [
        column
        for column, value in address_dict.items()
        if not any([value is None, column in exclude])
    ]
    displayname_full = ",".join(list(dict.fromkeys(positions)))

    return displayname_full.strip() if displayname_full else None


def get_displayname_short(address_dict: AddressDict) -> Optional[str]:
    pos1 = [x for x in DISPLAYNAME_SHORT_POS1 if address_dict[x] is not None] or [None]
    pos2 = [
        x
        for x in DISPLAYNAME_SHORT_POS2
        if not any([address_dict[x] is None, x == pos1[0]])
    ] or [None]

    if all([pos1[0], pos2[0]]):
        displayname_short = ",".join([pos1[0], pos2[0]])
    else:
        displayname_short = None
    return displayname_short.strip() if displayname_short else None


def gmaps_geocode_get_displaynames(address_dict: AddressDict) -> Optional[dict]:
    if not address_dict or not isinstance(address_dict, dict):
        return None

    exclude_columns = DISPLAYNAME_EXCLUDE

    if address_dict["county"] == "Oslo":
        exclude_columns = list(DISPLAYNAME_EXCLUDE)
        exclude_columns += ["county", "municipality"]

    return {
        "displayname_short": get_displayname_short(address_dict),
        "displayname_full": get_displayname_full(address_dict, exclude=exclude_columns),
    }


def gmaps_geocode_get_boundingbox(bbox_json: dict) -> Optional[BoundingBoxDict]:
    if not all(
        [
            bbox_json[NE],
            bbox_json[SW],
            isinstance(bbox_json[NE], dict),
            isinstance(bbox_json[SW], dict),
            bbox_json[NE][LAT],
            bbox_json[NE][LNG],
            bbox_json[SW][LAT],
            bbox_json[SW][LNG],
        ]
    ):
        return None

    bounds_lat = [bbox_json[NE][LAT], bbox_json[SW][LAT]]
    bounds_lng = [bbox_json[NE][LNG], bbox_json[SW][LNG]]

    corner_nw = (bbox_json[NE][LAT], bbox_json[SW][LNG])
    corner_ne = (bbox_json[NE][LAT], bbox_json[NE][LNG])
    corner_sw = (bbox_json[SW][LAT], bbox_json[SW][LNG])

    distances = {
        "ne_sw": distance.distance(corner_ne, corner_sw).meters,
        "ns": distance.distance(corner_nw, corner_sw).meters,
        "ew": distance.distance(corner_nw, corner_ne).meters,
    }

    return {
        "lat_min": min(bounds_lat),
        "lat_max": max(bounds_lat),
        "lng_min": min(bounds_lng),
        "lng_max": max(bounds_lng),
        "distances": distances,
    }


def clean_formatted_addr_field(
    formatted_addr: str,
    plus_code: str = None,
    country: str = None,
    country_code: str = None,
) -> str:
    if plus_code is not None:
        formatted_addr = formatted_addr.replace(plus_code, "").strip()

    if (
        country is not None
        and country_code is not None
        and re.search(country, formatted_addr, re.IGNORECASE)
    ):
        formatted_addr = re.sub(
            country,
            f"{PREPEND_COUNTRY_CODE}{country_code}",
            formatted_addr,
            flags=re.IGNORECASE,
        )

    return formatted_addr


def get_reverse_geotags_gmaps(latlng: LatLngTuple, levels: int = 5) -> GeocodeDict:
    def get_lvl_key(lvl: int) -> str:
        return f"{LVL_KEY_PREPEND}{lvl}"

    raw_data = GoogleMapsClient(key=GMAPS_TOKEN).reverse_geocode(latlng)

    json = [
        x
        for x in raw_data
        if not any(
            [
                x in NULL,
                not isinstance(x, dict),
                "place_id" not in x,
                x["place_id"] in NULL,
                "address_components" not in x,
                x["address_components"] in NULL,
                not isinstance(x["address_components"], list),
            ]
        )
    ]

    geotag_levels = []
    place_ids = []
    for res in json:
        if len(geotag_levels) == levels:
            break
        if any(
            [
                res["place_id"] in place_ids,
                "geometry" not in res,
                not isinstance(res["geometry"], dict),
                "bounds" not in res["geometry"],
            ]
        ):
            continue

        place_ids.append(res["place_id"])

        bbox = gmaps_geocode_get_boundingbox(res["geometry"]["bounds"])
        addr_dict = gmaps_geocode_get_address_dict(res["address_components"])

        if "formatted_address" in res:
            addr_dict["formatted_address"] = clean_formatted_addr_field(
                formatted_addr=res["formatted_address"],
                country=addr_dict["country"] if "country" in addr_dict else None,
                country_code=addr_dict["country_code"]
                if "country_code" in addr_dict
                else None,
                plus_code=addr_dict["plus_code"] if "plus_code" in addr_dict else None,
            )

        viewport = None
        if "viewport" in res["geometry"] and isinstance(
            res["geometry"]["viewport"], dict
        ):
            viewport = gmaps_geocode_get_viewport(res["geometry"]["viewport"])

        geotag_levels.append(
            {
                **bbox,
                **addr_dict,
                "viewport": viewport,
            }
        )

    geotag_levels.sort(key=lambda x: x["distances"]["ne_sw"])

    ret = {get_lvl_key(i + 1): geotag for i, geotag in enumerate(geotag_levels)}

    return ret


def parse_geo_str_to_decimal_tuple(string, include_altitude=False):
    return tuple(Point.from_string(string)[0 : (2 + include_altitude)])


def latlng_tuple_to_unicode_string(latlng, include_altitude=False):
    return Point(latlng).format_unicode(altitude=include_altitude)


# latlng = (
#     58.9767800,
#     5.7457600,
# )

# test = get_reverse_geotags_gmaps(latlng=latlng, levels=5)

# print(test)
