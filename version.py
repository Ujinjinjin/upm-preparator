import argparse
import json

parser = argparse.ArgumentParser(description='Write version of package to env-file', prog='version')

parser.add_argument('--version-file', dest='version_file', help='File storing version number', type=str, required=True)
parser.add_argument('--env-file', dest='env_file', help='File storing environment variables', type=str, required=True)


if __name__ == '__main__':
    args = parser.parse_args()

    with open(args.version_file, 'r', encoding='utf8') as file:
        version_dict = json.load(file)

    with open(args.env_file, 'a', encoding='utf8') as file:
        file.write(f'PKG_VERSION={version_dict["version"]}')
