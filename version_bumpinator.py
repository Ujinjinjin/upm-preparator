import json
import sys


if __name__ == '__main__':
    version_json_path = sys.argv[1]
    package_json_path = sys.argv[2]

    with open(version_json_path, 'r', encoding='utf8') as file:
        version_dict = json.load(file)
    
    with open(package_json_path, 'r', encoding='utf8') as file:
        package_dict = json.load(file)

    package_dict['version'] = version_dict['version']

    with open(package_json_path, 'w', encoding='utf8') as file:
        json.dump(package_dict, file, indent=4)