import argparse
import uuid
import glob
import os
import sys
import re
import json
from typing import List, Dict
from enum import Enum

parser = argparse.ArgumentParser(
    description='Generate proper .meta files for every file in project',
    prog='meta_makinator'
)

parser.add_argument('--package-file', dest='package_file', help='Path to package.json file', type=str, required=True)


class ImporterType(Enum):
    Folder = 1,
    Mono = 2,
    Text = 3,
    AsmDef = 4,
    Default = 5


MONO_IMPORTER_EXTENSIONS = [
    '.cs'
]

TEXT_IMPORTER_EXTENSIONS = [
    '.json',
    '.md',
    '.md',
]

ASMDEF_IMPORTER_EXTENSIONS = [
    '.asmdef'
]


def _get_uuid(_filename: str, _project_id: str) -> str:
    return str(uuid.uuid3(uuid.NAMESPACE_DNS, f'{_project_id}/{_filename}')).replace('-', '')


def _get_project_id(_package_json_path: str) -> str:
    with open(_package_json_path, 'r', encoding='utf8') as file:
        package_dict = json.load(file)
        return package_dict['name']


def _path_is_ignored(_path: str, _ignored_paths: List[str]) -> bool:
    for ignored_path in _ignored_paths:
        if re.match(ignored_path, _path):
            return True

    return False


def _get_file_paths(_root_path: str, _ignored_paths: List[str]) -> Dict[ImporterType, List[str]]:
    all_paths = [path.replace('\\', '/') for path in glob.glob(_root_path, recursive=True)]
    paths_dict: Dict[ImporterType, List[str]] = {
        ImporterType.Folder: list(),
        ImporterType.Mono: list(),
        ImporterType.Text: list(),
        ImporterType.AsmDef: list(),
        ImporterType.Default: list(),
    }

    for path in all_paths:
        if _path_is_ignored(path, _ignored_paths):
            continue

        if not (os.path.isfile(path)):
            paths_dict[ImporterType.Folder].append(path)
            continue

        extension = os.path.splitext(path)[-1]

        if extension in MONO_IMPORTER_EXTENSIONS:
            paths_dict[ImporterType.Mono].append(path)
            continue
        elif extension in TEXT_IMPORTER_EXTENSIONS:
            paths_dict[ImporterType.Text].append(path)
            continue
        elif extension in ASMDEF_IMPORTER_EXTENSIONS:
            paths_dict[ImporterType.AsmDef].append(path)
            continue

        paths_dict[ImporterType.Default].append(path)

    return paths_dict


def _get_meta_templates(_templates_folder: str):
    with open(f'{_templates_folder}/folder_meta_template') as file:
        folder_meta_template = file.read()
    with open(f'{_templates_folder}/mono_meta_template') as file:
        cs_meta_template = file.read()
    with open(f'{_templates_folder}/text_meta_template') as file:
        text_meta_template = file.read()
    with open(f'{_templates_folder}/asmdef_meta_template') as file:
        asmdef_meta_template = file.read()
    with open(f'{_templates_folder}/default_meta_template') as file:
        default_meta_template = file.read()

    return {
        ImporterType.Folder: folder_meta_template,
        ImporterType.Mono: cs_meta_template,
        ImporterType.Text: text_meta_template,
        ImporterType.AsmDef: asmdef_meta_template,
        ImporterType.Default: default_meta_template,
    }


def _generate_meta_files(_paths_dict: Dict[ImporterType, List[str]], _meta_templates: Dict[ImporterType, str], _project_id: str):
    for key, value in _paths_dict.items():
        template = _meta_templates[key]
        for path in value:
            guid = _get_uuid(path, _project_id)
            with open(f'{path}.meta', 'w', encoding='utf8') as file:
                file.write(template.format(guid))


if __name__ == '__main__':
    args = parser.parse_args()

    script_path_items = sys.argv[0].split('/')[:-1]
    script_path_items.append('templates')
    templates_folder = '/'.join(script_path_items)

    project_id = _get_project_id(args.package_file)

    ignored_paths = [
        r'.+\.meta',
        r'\.git\/.+',
        r'.*\/?upm-preparator.*',
        r'.*\/?temp.*',
    ]

    paths_dict = _get_file_paths('**', ignored_paths)
    templates = _get_meta_templates(templates_folder)

    _generate_meta_files(paths_dict, templates, project_id)
