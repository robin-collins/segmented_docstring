import re
import argparse
from pathlib import Path

def get_version_from_file(file_path):
    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.read()
        match = re.search(r'__version__\s*=\s*[\'"](\d+\.\d+\.\d+)[\'"]', content)
        if match:
            return tuple(map(int, match.group(1).split('.')))
    return (0, 0, 0)

def update_version_in_file(file_path, new_version):
    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.read()

    new_content = re.sub(
        r'(__version__\s*=\s*[\'"])\d+\.\d+\.\d+([\'"])',
        f'\\g<1>{new_version}\\g<2>',
        content
    )

    with open(file_path, 'w', encoding="utf-8") as file:
        file.write(new_content)

def update_version_in_toml(file_path, new_version):
    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.read()

    new_content = re.sub(
        r'(version\s*=\s*[\'"])\d+\.\d+\.\d+([\'"])',
        f'\\g<1>{new_version}\\g<2>',
        content
    )

    with open(file_path, 'w', encoding="utf-8") as file:
        file.write(new_content)

def increment_version(version):
    major, minor, patch = version
    return (major, minor, patch + 1)

def main():
    parser = argparse.ArgumentParser(description="Update version numbers")
    parser.add_argument('--building', action='store_true', help="Increment module versions")
    args = parser.parse_args()

    src_dir = Path('src/segmented_docstring')
    py_files = [f for f in src_dir.glob('*.py') if f.name != '__init__.py']

    if args.building:
        print("Incrementing module versions...")
        for file in py_files:
            current_version = get_version_from_file(file)
            new_version = increment_version(current_version)
            new_version_str = '.'.join(map(str, new_version))
            update_version_in_file(file, new_version_str)
            print(f"Updated {file.name} to version {new_version_str}")

    versions = [get_version_from_file(f) for f in py_files]
    new_version = tuple(sum(x) for x in zip(*versions))
    new_version_str = '.'.join(map(str, new_version))

    print(f"Calculated new version: {new_version_str}")

    # Update __init__.py
    init_file = src_dir / '__init__.py'
    update_version_in_file(init_file, new_version_str)
    print(f"Updated {init_file}")

    # Update setup.py
    setup_file = Path('setup.py')
    if setup_file.exists():
        update_version_in_file(setup_file, new_version_str)
        print(f"Updated {setup_file}")
    else:
        print(f"{setup_file} not found")

    # Update pyproject.toml
    toml_file = Path('pyproject.toml')
    if toml_file.exists():
        update_version_in_toml(toml_file, new_version_str)
        print(f"Updated {toml_file}")
    else:
        print(f"{toml_file} not found")

if __name__ == "__main__":
    main()
