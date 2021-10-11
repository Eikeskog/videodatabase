from googlemaps import Client as googlemapsClient
from geopy import distance, Point
from backend.dev_settings import GMAPS_TOKEN
from ...types.types import AddressDict, BoundingBoxDict, LatLngTuple


def gmaps_geocode_get_viewport(gmaps_viewport_json: dict) -> BoundingBoxDict:
    viewport = None
    if gmaps_viewport_json["northeast"] and gmaps_viewport_json["southwest"]:
        viewport_lat = (
            gmaps_viewport_json["northeast"]["lat"],
            gmaps_viewport_json["southwest"]["lat"],
        )
        viewport_lng = (
            gmaps_viewport_json["northeast"]["lng"],
            gmaps_viewport_json["southwest"]["lng"],
        )
        if all([*viewport_lat, *viewport_lng]):
            viewport = {
                "lat_min": min(viewport_lat),
                "lat_max": max(viewport_lat),
                "lng_min": min(viewport_lng),
                "lng_max": max(viewport_lng),
            }

    return viewport


def gmaps_geocode_get_address_dict(gmaps_address_components_json: dict) -> AddressDict:
    if gmaps_address_components_json is None:
        return None
    component_type_translations = {
        "administrative_area_level_2": "municipality",
        "administrative_area_level_1": "county",
    }
    remove_words = [
        "Fylke",
        "fylke",
        "Kommune",
        "kommune",
        "Municipality",
        "municipality",
        "County",
        "county",
    ]

    def clean_str(string):
        for word in remove_words:
            string = string.replace(word, "").strip()
        return string

    def get_column_name(component):
        component_type = get_component_type(component)
        if component_type in component_type_translations:
            return component_type_translations[component_type]
        else:
            return component_type

    def get_component_type(component_json):
        return str(
            max(
                [type for type in component_json["types"] if type != "political"],
                key=len,
            )
            if len(component_json["types"]) > 0
            else component_json["types"][0]
        )

    def get_component_value(component):
        return clean_str(max(set([component["short_name"], component["long_name"]])))

    def add_missing_dict_keys(parsed_dict):
        all_keys = [
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

        return {
            **parsed_dict,
            **{x: None for x in all_keys if x not in parsed_dict.keys()},
        }

    parsed_dict = add_missing_dict_keys(
        {
            get_column_name(component): get_component_value(component)
            for component in gmaps_address_components_json
        }
    )

    parsed_dict["country_code"] = [
        component["short_name"]
        for component in gmaps_address_components_json
        if "country" in component["types"]
    ][0]

    displaynames = gmaps_geocode_get_displaynames(parsed_dict)

    return {**parsed_dict, **displaynames}


def gmaps_geocode_get_displaynames(address_dict):
    if not address_dict or not isinstance(address_dict, dict):
        return None
    exclude_columns = [
        "postal_code",
        "street_number",
        "displayname_short",
        "displayname_full",
        "formatted_address",
        "country",
    ]

    if address_dict["county"] == "Oslo":
        exclude_columns += ["county", "municipality"]

    def get_displayname_full(address_dict):
        displayname_full = ",".join(
            list(
                dict.fromkeys(
                    [
                        column
                        for column, value in address_dict.items()
                        if not any([value is None, column in exclude_columns])
                    ]
                )
            )
        )

        return displayname_full.strip() if displayname_full else None

    def get_displayname_short(address_dict):
        pos1 = [
            x
            for x in [
                "postal_town",
                "locality",
                "municipality",
                "county",
                "postal_code",
            ]
            if address_dict[x] is not None
        ] or [None]

        pos2 = [
            x
            for x in ["county", "municipality", "country_code"]
            if not any([address_dict[x] is None, x == pos1[0]])
        ] or [None]

        displayname_short = (
            ",".join(
                list(dict.fromkeys([x for x in [pos1[0], pos2[0]] if x is not None]))
            )
            if any([pos1[0], pos2])
            else None
        )

        return displayname_short.strip() if displayname_short else None

    return dict(
        displayname_short=get_displayname_short(address_dict),
        displayname_full=get_displayname_full(address_dict),
    )


def format_reverse_geocode_gmaps(gmaps_geocode_raw: dict) -> AddressDict:
    if not gmaps_geocode_raw or not gmaps_geocode_raw["address_components"]:
        return None
    address_dict = gmaps_geocode_get_address_dict(
        gmaps_geocode_raw["address_components"]
    )
    return address_dict if address_dict else None


def gmaps_geocode_get_boundingbox(gmaps_bbox_bounds_json: dict) -> BoundingBoxDict:
    if not all(
        [
            gmaps_bbox_bounds_json["northeast"],
            gmaps_bbox_bounds_json["southwest"],
            isinstance(gmaps_bbox_bounds_json["northeast"], dict),
            isinstance(gmaps_bbox_bounds_json["southwest"], dict),
            gmaps_bbox_bounds_json["northeast"]["lat"],
            gmaps_bbox_bounds_json["northeast"]["lng"],
            gmaps_bbox_bounds_json["southwest"]["lat"],
            gmaps_bbox_bounds_json["southwest"]["lng"],
        ]
    ):
        return None

    bounds_lat = [
        gmaps_bbox_bounds_json["northeast"]["lat"],
        gmaps_bbox_bounds_json["southwest"]["lat"],
    ]
    bounds_lng = [
        gmaps_bbox_bounds_json["northeast"]["lng"],
        gmaps_bbox_bounds_json["southwest"]["lng"],
    ]

    point_nw = (
        gmaps_bbox_bounds_json["northeast"]["lat"],
        gmaps_bbox_bounds_json["southwest"]["lng"],
    )
    point_ne = (
        gmaps_bbox_bounds_json["northeast"]["lat"],
        gmaps_bbox_bounds_json["northeast"]["lng"],
    )
    point_sw = (
        gmaps_bbox_bounds_json["southwest"]["lat"],
        gmaps_bbox_bounds_json["southwest"]["lng"],
    )

    distances = {
        "ne_sw": distance.distance(point_ne, point_sw).meters,
        "ns": distance.distance(point_nw, point_sw).meters,
        "ew": distance.distance(point_nw, point_ne).meters,
    }

    return {
        "lat_min": min(bounds_lat),
        "lat_max": max(bounds_lat),
        "lng_min": min(bounds_lng),
        "lng_max": max(bounds_lng),
        "distances": distances,
    }


def get_reverse_geotags_gmaps(latlng: LatLngTuple, levels=5):
    null = [None, "", " "]
    gmaps = googlemapsClient(key=GMAPS_TOKEN)

    json = [
        x
        for x in gmaps.reverse_geocode(latlng)
        if not any(
            [
                x in null,
                not isinstance(x, dict),
                "place_id" not in x,
                x["place_id"] in null,
                "address_components" not in x,
                x["address_components"] in null,
                not isinstance(x["address_components"], list),
            ]
        )
    ]

    boxes = []
    place_ids = []

    for res in json:
        if res["place_id"] in place_ids:
            continue
        place_ids.append(res["place_id"])

        if not any(
            [
                len(boxes) == levels,
                "geometry" not in res,
                not isinstance(res["geometry"], dict),
                "bounds" not in res["geometry"],
            ]
        ):

            if not bool(res["address_components"]):
                return None

            if res["geometry"] and res["geometry"]["bounds"]:
                box = gmaps_geocode_get_boundingbox(res["geometry"]["bounds"])

            parsed_address = gmaps_geocode_get_address_dict(res["address_components"])

            if "viewport" in res["geometry"] and isinstance(
                res["geometry"]["viewport"], dict
            ):
                viewport = gmaps_geocode_get_viewport(res["geometry"]["viewport"])
            else:
                viewport = None

            boxes.append(
                dict(
                    **box,
                    **parsed_address,
                    viewport=viewport,
                )
            )

    boxes.sort(key=lambda x: x["distances"]["ne_sw"])

    return {"level_" + str(i + 1): box for i, box in enumerate(boxes)}


def parse_geo_str_to_decimal_tuple(string, include_altitude=False):
    return tuple(Point.from_string(string)[0 : (2 + include_altitude)])


def latlng_tuple_to_unicode_string(latlng, include_altitude=False):
    return Point(latlng).format_unicode(altitude=include_altitude)


# test = get_reverse_geotags_gmaps((58.507194, 5.798500))
# print(test)
