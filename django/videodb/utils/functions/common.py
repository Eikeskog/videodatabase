import re, decimal
from pathlib import Path

def is_all_numeric(args):
    return all(isinstance(x, (float, decimal.Decimal, int)) for x in args)

def is_numeric(arg):
    return isinstance(arg, (float, decimal.Decimal, int))

def is_list_or_tuple(arg):
    return isinstance(arg, (list, tuple))

def remove_leading_digits(str):
  return str.lstrip('0123456789.- ')

def filename_from_path(path):
  return path.split("/")[-1]

def root_dir_from_path(path, split_at=":/Filmprosjekter"):
  return path.split(split_at)[0] + split_at

def get_parent_dir(path):
  return str(Path(path).parent).replace("\\","/")

def rolltype_from_path(path, regex=r"\/[0-9][0-9]\. ([A-B]) Roll(\/|$)"):
  match = re.findall(regex, path, re.IGNORECASE)
  return match[0][0] if match else None

def foldername_from_path(dir_path):
  return dir_path.split("/")[-1]

def disk_from_path(path, regex=r"^([A-Za-z0-9\.\-_]\w+):\/"):
  match = re.findall(regex, path, re.IGNORECASE)
  return match[0] if match else None

def project_name_from_path(path, regex=r"^[A-Za-z0-9_\-\. ]\w+:\/[A-Za-z0-9_\-\. ]\w+\/[0-9][0-9] ([A-Åa-å0-9\-_\. ]+)(\/|$)"):
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

def project_main_dir_from_path(path, split_at="/01 Kamera råmateriale/"):
  return path.split(split_at)[0] if split_at in path else None

def rolltype_dir_from_path(path, re_split=r"[0-9][0-9]\. [A-B] Roll"):
  match = re.findall(re_split, path, re.IGNORECASE)
  if match:
    return re.split(re_split, path, re.IGNORECASE)[0] + match[0]
  return None

def is_root_dir_path(path, regex=r":/filmprosjekter($|\/$)"):
  return bool(re.search(regex,path, re.IGNORECASE))

def is_project_main_dir_path(path, regex=r":\/filmprosjekter\/[A-Åa-å0-9\.\-_ ]+($|\/$)"):
  return bool(re.search(regex,path, re.IGNORECASE))

def is_project_roll_dir_path(path, regex=r"\/*[A-Ba-b] roll(\/$|$)"):
  return bool(re.search(regex,path, re.IGNORECASE))

def is_valid_db_path(path, regex=r"^[A-Åa-å0-9\-_\. ]+:\/filmprosjekter(\/|$)"):
  return bool(re.search(regex,path, re.IGNORECASE))

def is_project_subdir_path(path):
    return not any([
        not is_valid_db_path(path),
        bool(re.search(r"kamera råmateriale(\/$|$)", path, re.IGNORECASE)),
        is_root_dir_path(path),
        is_project_main_dir_path(path),
        is_project_roll_dir_path(path)])