import glob
import os
import sys
import re
from typing import List, Dict

def _path_is_ignored(path: str, ignored_paths: List[str]) -> bool:
    for ignored_path in ignored_paths:
        if re.match(ignored_path, path):
            return True
    return False

def _get_paths(root_path: str, ignored_paths: List[str]) -> List[str]:
    all_paths = [path.replace('\\', '/') for path in glob.glob(root_path, recursive=True)]
    paths = list()

    for path in all_paths:
        if _path_is_ignored(path, ignored_paths):
            continue
        paths.append(path)
    return paths

def _delete_paths(paths_to_delete: List[str]) -> None:
    # delete all files
    for path in paths_to_delete:
        if os.path.isfile(path):
            os.remove(path)
    # delete all dirs
    for path in paths_to_delete:
        if os.path.isdir(path):
            os.rmdir(path)

def _move_from_package_folder_to_root(package_folder: str, paths_to_move: List[str]) -> None:
    for old_path in paths_to_move:
        new_path = old_path.replace(f'{package_folder}/', '')
        if len(new_path) > 0:
            os.replace(old_path, new_path)

def _remove_package_folder(package_folder: str) -> None:
    os.rmdir(package_folder)

if __name__ == '__main__':
    package_folder = sys.argv[1]
    package_folder_regex = package_folder.replace(".", "\\.")
    package_folder_regex = f'{package_folder_regex}.*'

    package_json_path = sys.argv[2]

    ignored_paths = [
        r'\.git\/.+',
        # r'.*\/?package\.json',
        # r'.*\/?version\.json',
        r'.*\/?upm-preparator.*',
        r'.*\/?temp.*',
        package_folder_regex
    ]

    paths_to_delete = _get_paths('**', ignored_paths)
    _delete_paths(paths_to_delete)

    paths_to_move = _get_paths(f'{package_folder}/**', list())
    paths_to_move.append(package_json_path)
    _move_from_package_folder_to_root(package_folder, paths_to_move)

    _remove_package_folder(package_folder)

