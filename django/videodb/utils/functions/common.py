import re
import decimal
from pathlib import Path
from typing import Any, Pattern


def is_all_numeric(args: Any) -> bool:
    return all(isinstance(x, (float, decimal.Decimal, int)) for x in args)


def is_numeric(arg: Any) -> bool:
    return isinstance(arg, (float, decimal.Decimal, int))


def is_list_or_tuple(arg: Any) -> bool:
    return isinstance(arg, (list, tuple))


def remove_leading_digits(string: str) -> str:
    if not isinstance(string, str):
        return None
    return string.lstrip("0123456789.- ")


def filename_from_path(path: str) -> str:
    if not isinstance(path, str):
        return None
    return path.split("/")[-1]


def root_dir_from_path(path: str, split_at: str = ":/Filmprosjekter") -> str:
    if not isinstance(path, str):
        return None
    return path.split(split_at)[0] + split_at


def get_parent_dir(path: str) -> str:
    if not isinstance(path, str):
        return None
    return str(Path(path).parent).replace("\\", "/")


def rolltype_from_path(
    path: str, regex: Pattern[str] = r"\/[0-9][0-9]\. ([A-B]) Roll(\/|$)"
) -> str:
    if not isinstance(path, str):
        return None
    match = re.findall(regex, path, re.IGNORECASE)
    return match[0][0] if match else None


def foldername_from_path(path: str) -> str:
    if not isinstance(path, str):
        return None
    return path.split("/")[-1]


def disk_from_path(path: str, regex: str = r"^([A-Za-z0-9\.\-_]\w+):\/") -> str:
    if not isinstance(path, str):
        return None
    match = re.findall(regex, path, re.IGNORECASE)
    return match[0] if match else None


def project_name_from_path(
    path: str,
    regex: str = (
        r"^[A-Za-z0-9_\-\. ]\w+:\/[A-Za-z0-9_\-\. ]\w+\/[0-9][0-9] ([A-Åa-å0-9\-_\. ]+)(\/|$)"
    ),
) -> str:
    if not isinstance(path, str):
        return None
    match = re.findall(regex, path, re.IGNORECASE)
    return match[0][0] if match else None


# def get_dir_dict_from_dir_path(dir_path):
#   dir_name = foldername_from_path(dir_path)
#   parent_path = parent_dir(dir_path)
#   disk = disk_from_path(dir_path)
#   rolltype = rolltype_from_path(dir_path)

#   return {
#     'dir_path': dir_path,
#     'dir_name': dir_name,
#     'parent_path': parent_path,
#     'disk': disk,
#     'rolltype': rolltype
#   }


def project_main_dir_from_path(
    path: str, split_at: str = "/01 Kamera råmateriale/"
) -> str:
    if not isinstance(path, str):
        return None
    return path.split(split_at)[0] if split_at in path else None


def rolltype_dir_from_path(
    path: str, re_split: str = r"[0-9][0-9]\. [A-B] Roll"
) -> str:
    if not isinstance(path, str):
        return None
    match = re.findall(re_split, path, re.IGNORECASE)
    if match:
        return re.split(re_split, path, re.IGNORECASE)[0] + match[0]
    return None


def is_root_dir_path(path: str, regex: str = r":/filmprosjekter($|\/$)") -> bool:
    if not isinstance(path, str):
        return None
    return bool(re.search(regex, path, re.IGNORECASE))


def is_project_main_dir_path(
    path: str, regex: str = r":\/filmprosjekter\/[A-Åa-å0-9\.\-_ ]+($|\/$)"
) -> bool:
    if not isinstance(path, str):
        return None
    return bool(re.search(regex, path, re.IGNORECASE))


def is_project_roll_dir_path(
    path: str, regex: str = r"\/*[A-Ba-b] roll(\/$|$)"
) -> bool:
    if not isinstance(path, str):
        return None
    return bool(re.search(regex, path, re.IGNORECASE))


def is_valid_db_path(
    path: str, regex: str = r"^[A-Åa-å0-9\-_\. ]+:\/filmprosjekter(\/|$)"
) -> bool:
    if not isinstance(path, str):
        return None
    return bool(re.search(regex, path, re.IGNORECASE))


def is_project_subdir_path(path: str) -> bool:
    if not isinstance(path, str):
        return None
    return not any(
        [
            not is_valid_db_path(path),
            bool(re.search(r"kamera råmateriale(\/$|$)", path, re.IGNORECASE)),
            is_root_dir_path(path),
            is_project_main_dir_path(path),
            is_project_roll_dir_path(path),
        ]
    )
