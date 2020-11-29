import argparse
import json

parser = argparse.ArgumentParser(
    description='Bump project version and write version to env-file',
    prog='version_bumpinator'
)

parser.add_argument('--version-file', dest='version_file', help='File storing version number', type=str, required=True)
parser.add_argument('--package-file', dest='package_file', help='Path to package.json file', type=str, required=True)
parser.add_argument('--env-file', dest='env_file', help='File storing environment variables', type=str, required=True)


if __name__ == '__main__':
    args = parser.parse_args()

    with open(args.version_file, 'r', encoding='utf8') as file:
        version_dict = json.load(file)
    
    with open(args.package_file, 'r', encoding='utf8') as file:
        package_dict = json.load(file)

    package_dict['version'] = version_dict['version']

    with open(args.package_file, 'w', encoding='utf8') as file:
        json.dump(package_dict, file, indent=2)
    
    with open(args.env_file, 'a', encoding='utf8') as file:
        file.write(f'PKG_VERSION={version_dict["version"]}')
