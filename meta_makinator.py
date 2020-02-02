import uuid
import glob
import os
import sys
import re
from typing import List, Dict
from enum import Enum

class PathType(Enum):
    CsScript = 1,
    TextFile = 2,
    Folder = 3

def _get_uuid(filename: str) -> str:
    return str(uuid.uuid3(uuid.NAMESPACE_DNS, filename)).replace('-', '')

def _path_is_ignored(path: str, ignored_paths: List[str]) -> bool:
    for ignored_path in ignored_paths:
        if re.match(ignored_path, path):
            return True

    return False

def _get_file_paths(root_path: str, ignored_paths: List[str]) -> Dict[PathType, List[str]]:
    all_paths = [path.replace('\\', '/') for path in glob.glob(root_path, recursive=True)]
    paths_dict: Dict[PathType, List[str]] = {
        PathType.CsScript: list(),
        PathType.TextFile: list(),
        PathType.Folder: list(),
    }

    for path in all_paths:
        if _path_is_ignored(path, ignored_paths):
            continue
        
        if not (os.path.isfile(path)):
            paths_dict[PathType.Folder].append(path)
            continue
        
        if path[-3:] == '.cs':
            paths_dict[PathType.CsScript].append(path)
            continue

        paths_dict[PathType.TextFile].append(path)

    return paths_dict

def _get_meta_templates(templates_folder: str):
    with open(f'{templates_folder}/cs_meta_template') as file:
        cs_meta_template = file.read()
    with open(f'{templates_folder}/folder_meta_template') as file:
        folder_meta_template = file.read()
    with open(f'{templates_folder}/text_meta_template') as file:
        text_meta_template = file.read()
    
    return {
        PathType.CsScript: cs_meta_template,
        PathType.TextFile: text_meta_template,
        PathType.Folder: folder_meta_template
    }

def _generate_meta_files(paths_dict: Dict[PathType, List[str]], meta_templates: Dict[PathType, str]):
    for key, value in paths_dict.items():
        temaplate = meta_templates[key]
        for path in value:
            guid = _get_uuid(path)
            with open(f'{path}.meta', 'w', encoding='utf8') as file:
                file.write(temaplate.format(guid))

if __name__ == '__main__':
    script_path_items = sys.argv[0].split('/')[:-1]
    script_path_items.append('templates')
    templates_folder = '/'.join(script_path_items)

    ignored_paths = [
        r'.+\.meta', 
        r'\.git\/.+', 
        r'.*\/?upm-preparator.*'
    ]

    paths_dict = _get_file_paths('**', ignored_paths)
    templates = _get_meta_templates(templates_folder)

    _generate_meta_files(paths_dict, templates)