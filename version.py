import json
import sys
import os


if __name__ == '__main__':
    version_json_path = sys.argv[1]

    with open(version_json_path, 'r', encoding='utf8') as file:
        version_dict = json.load(file)

    new_version = version_dict['version']
    
    os.system(f'echo ::set-env name=PKG_VERSION::{new_version}')
