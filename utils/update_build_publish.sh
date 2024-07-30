#!/bin/bash

check_and_activate_pyenv_segdoc() {
    # Check if the pyenv segdoc is already active
    if [[ "$(pyenv version-name)" == "segdoc" ]]; then
        echo 'pyenv segdoc is already active'
        return 0
    else
        echo 'activating pyenv segdoc'
        pyenv activate segdoc
        return $?
    fi
}

build_python_package() {
    local package_dir="${1:?Package directory must be provided}"
    local build_output
    local build_status

    # Change to the package directory
    cd "${package_dir}" || return 1

    # Ensure the directory contains a pyproject.toml or setup.py file
    if [[ ! -f "pyproject.toml" && ! -f "setup.py" ]]; then
        echo "Error: Neither pyproject.toml nor setup.py found in ${package_dir}" >&2
        return 1
    fi

    # Clean up any existing build artifacts
    echo "Cleaning up existing build artifacts..."
    rm -rf build dist ./*.egg-info

    # Build the package
    echo "Building the Python package..."
    build_output=$(python -m build 2>&1)
    build_status=$?

    if [[ ${build_status} -ne 0 ]]; then
        echo "Error: Package build failed" >&2
        echo "Build output:" >&2
        echo "${build_output}" >&2
        return ${build_status}
    fi

    # Check if the build was successful
    if [[ -d "dist" && "$(ls -A dist)" ]]; then
        echo "Package built successfully"
        echo "Built artifacts:"
        ls -l dist
    else
        echo "Error: No distribution files found after build" >&2
        return 1
    fi

    return 0
}

upload_to_pypi() {
  twine upload dist/*
}

main() {
SCRIPT_DIR="$(cd -- "$(dirname "$0")" >/dev/null 2>&1 || exit; pwd -P)"
PROJECT_DIR=$(cd -- "${SCRIPT_DIR}/.." &>/dev/null || exit && pwd)

  # change to PROJECT_DIR
  if ! cd "${PROJECT_DIR}"; then
    echo "Error: Unable to change to project directory" >&2
    exit 1
  fi
  
  if ! check_and_activate_pyenv_segdoc; then
    echo "Error: Failed to activate pyenv segdoc" >&2
    exit 1
  fi

  if ! python utils/update_versions.py --build; then
    echo 'update_versions.py failed'
    exit 1
  fi

  echo 'update_versions.py succeeded'
  if build_python_package "${PROJECT_DIR}"; then
    echo "Build successful"
    upload_to_pypi
  else
    echo "Build failed"
    exit 1
  fi
}

main
