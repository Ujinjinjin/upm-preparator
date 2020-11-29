import argparse
import glob
import os
import re
from typing import List

parser = argparse.ArgumentParser(
    description='Change structure of project to match UPM requirements',
    prog='structure_changinator'
)

parser.add_argument('--package-root', dest='package_root', help='Root path of package', type=str, required=True)


def _path_is_ignored(path: str, ignored_paths: List[str]) -> bool:
    for ignored_path in ignored_paths:
        if re.match(ignored_path, path):
            return True
    return False


def _get_paths(root_path: str, ignored_paths: List[str], files_in_prior: bool = False, files_only: bool = False) -> List[str]:
    all_paths = [path.replace('\\', '/') for path in glob.glob(root_path, recursive=True)]
    paths = list()

    for path in all_paths:
        if _path_is_ignored(path, ignored_paths):
            continue
        paths.append(path)

    if files_in_prior:
        files = [path for path in paths if os.path.isfile(path)]
        dirs = [path for path in paths if os.path.isdir(path)]
        dirs.sort(key=lambda x: x.count('/'))
        dirs.reverse()

        paths = files + dirs

    if files_only:
        paths = [path for path in paths if os.path.isfile(path)]

    return paths


def _delete_paths(_paths_to_delete: List[str]) -> None:
    # delete all files
    for path in _paths_to_delete:
        if os.path.isfile(path):
            os.remove(path)
    # delete all dirs
    for path in _paths_to_delete:
        if os.path.isdir(path):
            os.rmdir(path)


def _move_from_package_folder_to_root(_package_folder: str, _paths_to_move: List[str]) -> None:
    for old_path in _paths_to_move:
        new_path = old_path.replace(f'{_package_folder}/', '')
        if len(new_path) > 0:
            if len(os.path.dirname(new_path)) > 0:
                os.makedirs(os.path.dirname(new_path), exist_ok=True)
            os.replace(old_path, new_path)


if __name__ == '__main__':
    args = parser.parse_args()

    package_folder_regex = args.package_root.replace(".", "\\.")
    package_folder_regex = f'{package_folder_regex}.*'

    ignored_to_delete_paths = [
        r'\.git\/.+',
        # r'.*\/?package\.json',
        # r'.*\/?version\.json',
        r'.*\/?upm-preparator.*',
        r'.*\/?temp.*',
        package_folder_regex
    ]

    paths_to_delete = _get_paths('**', ignored_to_delete_paths, files_in_prior=True)
    _delete_paths(paths_to_delete)

    ignored_to_move_paths = [
        r'.*\/?package\.json',
        r'.*\/?version\.json',
    ]

    paths_to_move = _get_paths(f'{args.package_root}/**', ignored_to_move_paths, files_only=True)
    _move_from_package_folder_to_root(args.package_root, paths_to_move)
